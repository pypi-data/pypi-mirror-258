import base64
from dataclasses import dataclass
import json
from math import ceil
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from flow_tuning.providers.base import BaseProvider
from flow_tuning.providers.base import FunctionConfig
from flow_tuning.providers.base import FunctionInvocationResult
from flow_tuning.providers.base import WorkflowDescription
from flow_tuning.providers.base import WorkflowStepDescription
from flow_tuning.utils.console import console


@dataclass
class AwsFunctionInvocationResult(FunctionInvocationResult):
  raw_log: str
  memory_size: int
  max_memory_used: int
  init_duration: float


def asl_to_workflow_description(
    asl: Dict[str, Any], prefix: str = '$$'
) -> WorkflowDescription:
  start_at = asl.get('StartAt', '')
  states = asl.get('States', {})
  steps: List[WorkflowStepDescription] = []

  for state_name, state_info in states.items():
    step_id = f"{prefix}.{state_name}"
    step_type = state_info.get('Type').lower()

    if step_type == 'task':
      resource = state_info.get('Resource', '')
      function_id = None
      if resource.startswith('arn:aws:lambda'):
        function_id = resource
      steps.append(
          WorkflowStepDescription(
              step_id=step_id, type='function', function_id=function_id
          )
      )

    elif step_type == 'parallel':
      branches = {}
      for i, branch in enumerate(state_info.get('Branches', [])):
        branch_id = f"{step_id}.branch-{i}"
        branch_description = asl_to_workflow_description(
            branch, prefix=branch_id
        )
        branches[branch_id] = branch_description
      steps.append(
          WorkflowStepDescription(
              step_id=step_id, type='parallel', branches=branches
          )
      )

    elif step_type == 'map':
      iterator = state_info.get('Iterator', {})
      workflow = asl_to_workflow_description(
          iterator, prefix=f"{step_id}.workflow"
      )
      steps.append(
          WorkflowStepDescription(
              step_id=step_id, type='map', workflow=workflow
          )
      )

    # Add more cases as needed for 'Choice', 'Wait', etc.

  return WorkflowDescription(workflow_id=start_at, steps=steps)


class AwsProvider(BaseProvider):

  def __init__(self):
    self.lambda_client = boto3.client('lambda')
    self.sfn_client = boto3.client('stepfunctions')

  def _get_lambda_base_cost(self, region: str, architecture: str):
    data = {
        'x86_64': {
            'ap-east-1': 2.9e-9,
            'af-south-1': 2.8e-9,
            'me-south-1': 2.6e-9,
            'eu-south-1': 2.4e-9,
            'ap-northeast-3': 2.7e-9,
            'cn-north-1': 0.0000000142,
            'cn-northwest-1': 0.0000000142,
            'default': 2.1e-9
        },
        'arm64': {
            'default': 1.7e-9
        }
    }
    data = data.get(architecture, data['x86_64'])
    data = data.get(region, data['default'])
    return data

  def _get_lambda_cost(self, base_cost: float, duration: float, memory: int):
    # See AWS Lambda Power Tuning source code for the formula
    return base_cost * ceil(duration) * memory / 128

  def parse_lambda_function_arn(self, arn: str) -> Dict[str, str]:
    parts = arn.split(':')
    if len(parts) < 7 or len(parts) > 8:
      raise ValueError(f'Invalid lambda function ARN: {arn}')
    _, _, _, region, account_id, _, function_name, *qualifier = parts
    return {
        'region': region,
        'account_id': account_id,
        'function_name': function_name,
        'qualifier': qualifier[0] if qualifier else ''
    }

  def arn_to_region(self, arn: str) -> str:
    return self.parse_lambda_function_arn(arn)['region']

  async def configure_function(
      self, function_id: str, qualifier: str, config: FunctionConfig
  ) -> None:
    try:
      # Update function configuration
      self.lambda_client.update_function_configuration(
          FunctionName=function_id, MemorySize=config.memory
      )
      console.log(f"Updated function {function_id} to memory {config.memory}")

      # Wait for the function to be updated with interval 100ms
      waiter = self.lambda_client.get_waiter('function_updated')
      waiter.wait(FunctionName=function_id)

      # Publish a new version
      response = self.lambda_client.publish_version(FunctionName=function_id)
      version = response['Version']
      console.log(f"Published version {version} for function {function_id}")

      # Update or create alias
      try:
        self.lambda_client.update_alias(
            FunctionName=function_id, Name=qualifier, FunctionVersion=version
        )
      except self.lambda_client.exceptions.ResourceNotFoundException:
        self.lambda_client.create_alias(
            FunctionName=function_id, Name=qualifier, FunctionVersion=version
        )

      console.log(
          f"Configured alias {qualifier} for version {version} of function {function_id}"
      )
    except ClientError as error:
      console.log(f"Error configuring function: {error}")

  async def deconfigure_function(
      self, function_id: str, qualifier: str
  ) -> None:
    try:
      # Delete the specified alias and its associated version
      alias_info = self.lambda_client.get_alias(
          FunctionName=function_id, Name=qualifier
      )
      function_version = alias_info['FunctionVersion']

      self.lambda_client.delete_alias(FunctionName=function_id, Name=qualifier)
      console.log(f"Deleted alias {qualifier} for function {function_id}")

      self.lambda_client.delete_function(
          FunctionName=function_id, Qualifier=function_version
      )
      console.log(
          f"Deleted version {function_version} of function {function_id}"
      )
    except ClientError as error:
      console.log(f"Error deconfiguring function: {error}")

  async def invoke_function(
      self, function_id: str, qualifier: str, payload: Any
  ) -> FunctionInvocationResult:
    try:
      response = self.lambda_client.invoke(
          FunctionName=function_id,
          Qualifier=qualifier,
          Payload=json.dumps(payload),
          LogType='Tail'
      )
      log_result = base64.b64decode(response['LogResult']).decode('utf-8')
      log_lines = log_result.split('\n')
      report_line = next(
          (line for line in log_lines if line.startswith('REPORT RequestId:')),
          None
      )
      if not report_line:
        raise ValueError('Report line not found')

      def parse_field(key: str, unit: str) -> Optional[str]:
        line = report_line.split(f'{key}: ')
        if len(line) < 2:
          return None
        return line[1].split(f' {unit}')[0].strip()

      duration = float(parse_field('Duration', 'ms') or '0')
      billed_duration = float(parse_field('Billed Duration', 'ms') or '0')
      memory_size = int(parse_field('Memory Size', 'MB') or '0')
      max_memory_used = int(parse_field('Max Memory Used', 'MB') or '0')
      init_duration = float(parse_field('Init Duration', 'ms') or '0')

      # Construct and return a FunctionInvocationResult object
      return AwsFunctionInvocationResult(
          output=response.get('Payload', {}
                             ).read().decode('utf-8'),  # Assuming JSON response
          duration=duration,
          billed_duration=billed_duration,
          cost=self._get_lambda_cost(
              self._get_lambda_base_cost(
                  self.arn_to_region(function_id), 'x86_64'
              ), duration, memory_size
          ),
          raw_log=log_result,
          memory_size=memory_size,
          max_memory_used=max_memory_used,
          init_duration=init_duration
      )
    except ClientError as error:
      console.log(f"Error invoking function: {error}")
      raise error

  # Additional methods (describe_workflow, invoke_workflow, etc.) would be translated similarly,
  # adapting AWS SDK calls to their Boto3 equivalents and handling responses accordingly.

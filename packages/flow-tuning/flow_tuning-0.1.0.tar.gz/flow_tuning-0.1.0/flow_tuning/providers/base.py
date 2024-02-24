from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional


@dataclass
class FunctionConfig:
  # Memory in MB
  memory: int


@dataclass
class FunctionInvocationResult:
  # The function output
  output: Any
  # duration (may include environment setup time, etc.)
  duration: float
  # billed duration
  billed_duration: float
  # the total cost
  cost: float


@dataclass
class WorkflowStepDescription:
  step_id: str
  type: Literal["fixed", "function", "branch", "parallel", "map"]
  function_id: Optional[str] = None
  branches: Optional[Dict[str, "WorkflowDescription"]] = None
  workflow: Optional["WorkflowDescription"] = None


@dataclass
class WorkflowDescription:
  workflow_id: str
  steps: List[WorkflowStepDescription]


@dataclass
class WorkflowStepInvocationResult:
  step_id: str
  duration: float
  billed_duration: float
  cost: float
  branched_results: Optional[Dict[str, "WorkflowInvocationResult"]]
  mapped_results: Optional[List["WorkflowInvocationResult"]]


@dataclass
class WorkflowInvocationResult:
  workflow_id: str
  steps: List[WorkflowStepInvocationResult]


class BaseProvider(ABC):

  @abstractmethod
  async def configure_function(
      self, function_id: str, qualifier: str, config: FunctionConfig
  ) -> None:
    pass

  @abstractmethod
  async def deconfigure_function(
      self, function_id: str, qualifier: str
  ) -> None:
    pass

  @abstractmethod
  async def invoke_function(
      self, function_id: str, qualifier: str, payload: Any
  ) -> FunctionInvocationResult:
    pass

  # @abstractmethod
  # async def describe_workflow(self, workflow_id: str) -> WorkflowDescription:
  #   pass

  # @abstractmethod
  # async def invoke_workflow(
  #     self, workflow_id: str, description: WorkflowDescription, payload: Any
  # ) -> WorkflowInvocationResult:
  #   pass

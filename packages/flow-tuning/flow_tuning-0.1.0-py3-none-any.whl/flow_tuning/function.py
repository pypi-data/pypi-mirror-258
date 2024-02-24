import asyncio
import random
import string
from typing import Any, Dict, List, Literal, NamedTuple, Tuple

from flow_tuning.generators.base import BaseGenerator
from flow_tuning.providers.base import BaseProvider
from flow_tuning.providers.base import FunctionConfig
from flow_tuning.providers.base import FunctionInvocationResult
from flow_tuning.utils.console import console
from flow_tuning.utils.module_loader import load_class


class FunctionTuningInitializerInput(NamedTuple):
  provider: str
  function_id: str
  configs: Dict[str, FunctionConfig]


class FunctionTuningInitializerOutput(NamedTuple):
  configured_qualifiers: Dict[str, str]


async def initialize(
    input: FunctionTuningInitializerInput
) -> FunctionTuningInitializerOutput:
  Provider = load_class(BaseProvider, input.provider)
  provider = Provider()  # type: ignore
  configured_qualifiers: Dict[str, str] = {}
  rand_str = ''.join(
      random.choices(string.ascii_lowercase + string.digits, k=6)
  )
  for key, function_config in input.configs.items():
    qualifier = f"FT-{rand_str}-{key}"
    await provider.configure_function(
        function_id=input.function_id,
        qualifier=qualifier,
        config=function_config
    )
    configured_qualifiers[key] = qualifier
  return FunctionTuningInitializerOutput(configured_qualifiers)


class FunctionTuningExecutorInput(NamedTuple):
  provider: str
  function_id: str
  qualifier: str
  generator: str
  generator_input: Any
  invocation_mode: Literal['serial', 'parallel']


class FunctionTuningExecutorOutput(NamedTuple):
  results: List[FunctionInvocationResult]


async def execute(
    input: FunctionTuningExecutorInput
) -> FunctionTuningExecutorOutput:
  Provider = load_class(BaseProvider, input.provider)
  provider = Provider()  # type: ignore
  Generator = load_class(BaseGenerator, input.generator)
  generator = Generator()  # type: ignore
  results: List[FunctionInvocationResult] = []
  batch_count = 0
  async for batch in generator.generate_batch(input.generator_input):
    batch_count += 1
    console.log(
        f"Executing qualifier={input.qualifier}",
        f"batch={batch_count}(x{len(batch)})", f"in {input.invocation_mode}"
    )
    if input.invocation_mode == 'serial':
      for payload in batch:
        result = await provider.invoke_function(
            function_id=input.function_id,
            qualifier=input.qualifier,
            payload=payload
        )
        results.append(result)
    elif input.invocation_mode == 'parallel':
      tasks = map(
          lambda payload: provider.invoke_function(
              function_id=input.function_id,
              qualifier=input.qualifier,
              payload=payload
          ), batch
      )
      results.extend(await asyncio.gather(*tasks))
  return FunctionTuningExecutorOutput(results)


class FunctionTuningDispatcherInput(NamedTuple):
  provider: str
  function_id: str
  configs: Dict[str, FunctionConfig]
  configured_qualifiers: Dict[str, str]
  generator: str
  generator_input: Any
  invocation_mode: Literal['serial', 'parallel']
  execution_mode: Literal['serial', 'parallel']


class FunctionTuningDispatcherOutput(NamedTuple):
  results: Dict[str, FunctionTuningExecutorOutput]


async def dispatch(
    input: FunctionTuningDispatcherInput
) -> FunctionTuningDispatcherOutput:
  load_class(BaseProvider, input.provider)
  load_class(BaseGenerator, input.generator)
  results: Dict[str, FunctionTuningExecutorOutput] = {}
  if input.execution_mode == 'serial':
    for key, qualifier in input.configured_qualifiers.items():
      console.log(f"Dispatching for key={key}, qualifier={qualifier}")
      results[key] = await execute(
          FunctionTuningExecutorInput(
              provider=input.provider,
              function_id=input.function_id,
              qualifier=qualifier,
              generator=input.generator,
              generator_input=input.generator_input,
              invocation_mode=input.invocation_mode
          )
      )
  else:
    keys = list(input.configured_qualifiers.keys())
    tasks = map(
        lambda key: execute(
            FunctionTuningExecutorInput(
                provider=input.provider,
                function_id=input.function_id,
                qualifier=input.configured_qualifiers[key],
                generator=input.generator,
                generator_input=input.generator_input,
                invocation_mode=input.invocation_mode
            )
        ), keys
    )
    console.log("Parallel Dispatch started...")
    results = dict(zip(keys, await asyncio.gather(*tasks)))
  return FunctionTuningDispatcherOutput(results)


class FunctionTuningCleanerInput(NamedTuple):
  provider: str
  function_id: str
  configured_qualifiers: Dict[str, str]


async def clean(input: FunctionTuningCleanerInput):
  Provider = load_class(BaseProvider, input.provider)
  provider = Provider()  # type: ignore
  for qualifier in input.configured_qualifiers.values():
    await provider.deconfigure_function(
        function_id=input.function_id, qualifier=qualifier
    )


class FunctionTuningAnalyserInput(NamedTuple):
  provider: str
  function_id: str
  configs: Dict[str, FunctionConfig]
  configured_qualifiers: Dict[str, str]
  dispatcher_output: FunctionTuningDispatcherOutput
  weight: float


class FunctionTuningAnalyserOutput(NamedTuple):
  best_config_key: str
  best_duration: float
  best_cost: float


async def analyse(
    input: FunctionTuningAnalyserInput
) -> FunctionTuningAnalyserOutput:
  memory_values = input.configs.values()
  memory_values = map(lambda x: x.memory, memory_values)
  memory_values = sorted(memory_values)
  memory_to_results: Dict[int, Tuple[str, List[FunctionInvocationResult]]] = {}
  for key, config in input.configs.items():
    results = input.dispatcher_output.results[key].results
    memory_to_results[config.memory] = (key, results)
  points: List[Tuple[int, float, float, str]] = []
  for memory in memory_values:
    key, results = memory_to_results[memory]
    total_duration = 0.0
    total_cost = 0.0
    for result in results:
      total_duration += result.billed_duration
      total_cost += result.cost
    avg_duration = total_duration / len(results)
    avg_cost = total_cost / len(results)
    points.append((memory, avg_duration, avg_cost, key))
  console.log("Calculated points:")
  console.log(points)
  max_duration = max(map(lambda x: x[1], points))
  max_cost = max(map(lambda x: x[2], points))
  sorted_points = sorted(
      points,
      key=lambda x: ((x[1] * (1 - input.weight) / max_duration) +
                     (x[2] * input.weight / max_cost))
  )
  console.log("Best point found:")
  console.log(sorted_points[0])
  _, best_duration, best_cost, best_config_key = sorted_points[0]
  return FunctionTuningAnalyserOutput(
      best_config_key=best_config_key,
      best_duration=best_duration,
      best_cost=best_cost
  )

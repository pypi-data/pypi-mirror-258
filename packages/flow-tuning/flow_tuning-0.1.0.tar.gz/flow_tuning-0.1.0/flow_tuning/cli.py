import asyncio
from dataclasses import dataclass
from typing import Annotated, Any, Dict, List, Literal

import typer
from yaml import load

from flow_tuning.utils.module_loader import load_class

try:
  from yaml import CLoader as Loader
except ImportError:
  from yaml import Loader

import flow_tuning.function as ft_func
from flow_tuning.providers.base import FunctionConfig
from flow_tuning.utils.console import console

app = typer.Typer()


@dataclass
class FunctionTuningConfig:
  provider: str
  function_id: str
  configs: List[FunctionConfig]
  generator: str
  generator_input: Any
  invocation_mode: Literal['serial', 'parallel']
  execution_mode: Literal['serial', 'parallel']
  weight: float


@app.command()
def function(config_path: Annotated[str, typer.Option("--config", "-c")]):
  with open(config_path, 'r') as f:
    config_data = load(f, Loader)
  config_data['configs'] = [
      FunctionConfig(**config) for config in config_data['configs']
  ]
  config = FunctionTuningConfig(**config_data)

  # Ensure classes can be loaded
  console.log(
      "Using provider=", load_class(ft_func.BaseProvider, config.provider)
  )
  console.log(
      "Using generator=", load_class(ft_func.BaseGenerator, config.generator)
  )

  function_configs: Dict[str, FunctionConfig] = {}
  for i, function_config in enumerate(config.configs):
    function_configs[f'config-{i}'] = function_config

  async def _wrapper():
    initializer_output = await ft_func.initialize(
        ft_func.FunctionTuningInitializerInput(
            provider=config.provider,
            function_id=config.function_id,
            configs=function_configs
        )
    )
    console.log("Function qualifiers generated")

    dispatcher_output = await ft_func.dispatch(
        ft_func.FunctionTuningDispatcherInput(
            provider=config.provider,
            function_id=config.function_id,
            configs=function_configs,
            configured_qualifiers=initializer_output.configured_qualifiers,
            generator=config.generator,
            generator_input=config.generator_input,
            invocation_mode=config.invocation_mode,
            execution_mode=config.execution_mode,
        )
    )
    console.log("Function dispatched")

    await ft_func.clean(
        ft_func.FunctionTuningCleanerInput(
            provider=config.provider,
            function_id=config.function_id,
            configured_qualifiers=initializer_output.configured_qualifiers
        )
    )
    console.log("Function qualifiers cleaned")

    analyser_output = await ft_func.analyse(
        ft_func.FunctionTuningAnalyserInput(
            provider=config.provider,
            function_id=config.function_id,
            configs=function_configs,
            configured_qualifiers=initializer_output.configured_qualifiers,
            dispatcher_output=dispatcher_output,
            weight=config.weight
        )
    )
    console.log("Function analysis completed")
    console.log(analyser_output)

  asyncio.run(_wrapper())


@app.command()
def workflow(config: str):
  with open(config, 'r') as f:
    config_data = load(f, Loader)
  print(config_data)


if __name__ == "__main__":
  app()

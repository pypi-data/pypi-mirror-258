import importlib
import importlib.util
from typing import ClassVar


def load_internal_module(module_name: str):
  module = importlib.import_module(module_name, 'flow_tuning')
  return module


def load_from_module(module_path, name):
  spec = importlib.util.spec_from_file_location("user_specified", module_path)
  if spec is None or spec.loader is None:
    return

  module = importlib.util.module_from_spec(spec)
  if module is None:
    return

  spec.loader.exec_module(module)

  if hasattr(module, name):
    return getattr(module, name)
  else:
    return


def load_class[T: type](cls: T, name: str) -> T:
  type = cls.__name__.split('Base')[1].lower()
  name, *cls_name = name.split('#')
  if not cls_name:
    module = load_internal_module(f'flow_tuning.{type}s.{name}')
    result = getattr(module, f'{name.capitalize()}{type.capitalize()}')
  else:
    result = load_from_module(name, *cls_name)
  if not result:
    raise ImportError(f'Could not find class {name} in module {cls_name}')
  if issubclass(result, cls):
    return result
  raise ImportError(f'Class {result} is not a subclass of {cls}')

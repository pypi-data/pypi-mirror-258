from abc import ABC
from abc import abstractmethod
from typing import Any, AsyncIterable, List


class BaseGenerator(ABC):

  @abstractmethod
  def generate_batch(self, input: Any) -> AsyncIterable[List[Any]]:
    pass

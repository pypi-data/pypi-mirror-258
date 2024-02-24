from typing import Any, AsyncIterable, Dict, List

from flow_tuning.generators.base import BaseGenerator


class BasicGeneratorInput:

  def __init__(self, total: int, payloads: List[Any]):
    self.total = total
    self.payloads = payloads


class BasicGenerator(BaseGenerator):

  async def generate_batch(self, input: Any) -> AsyncIterable[List[Any]]:
    input_data = BasicGeneratorInput(**input)  # Assuming input is a dictionary
    for i in range(input_data.total):
      yield [input_data.payloads[i % len(input_data.payloads)]]

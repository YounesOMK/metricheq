from typing import Callable, List, Optional, Union

from pydantic import BaseModel


class Metric(BaseModel):
    value: Optional[Union[int, float, bool]]

    def satisfies(self, criterion: Callable[["Metric"], bool]) -> bool:
        if self.value is None:
            return False
        return criterion(self)

    def satisfies_all(self, criteria: List[Callable[["Metric"], bool]]) -> bool:
        if self.value is None:
            return False
        return all(criterion(self) for criterion in criteria)

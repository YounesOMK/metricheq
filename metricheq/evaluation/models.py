from abc import ABC, abstractmethod
from typing import List, Optional, Union

from pydantic import BaseModel


class Metric(BaseModel):
    value: Optional[Union[int, float, bool]]

    def satisfies(self, criterion) -> bool:
        if self.value is None:
            return False

        if callable(criterion):
            return criterion(self.value)
        elif isinstance(criterion, Criterion):
            return criterion.is_satisfied_by(self)
        else:
            raise ValueError("Criterion must be a callable or an instance of Criterion")

    def satisfies_all(self, criteria: List["Criterion"]) -> bool:
        if self.value is None:
            return False
        return all(self.satisfies(criterion) for criterion in criteria)


class Criterion(ABC):
    @abstractmethod
    def is_satisfied_by(self, metric: Metric) -> bool:
        pass

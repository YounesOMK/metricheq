from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel


class Metric(BaseModel):
    value: Optional[Union[int, float, bool]]

    def satisfies(self, criterion: "Criterion") -> bool:
        if self.value is None:
            return False
        return criterion.is_satisfied_by(self)

    def satisfies_all(self, criteria: List["Criterion"]) -> bool:
        if self.value is None:
            return False
        return all(self.satisfies(criterion) for criterion in criteria)


class Criterion(ABC):
    @abstractmethod
    def is_satisfied_by(self, metric: Metric) -> bool:
        pass

from abc import ABC, abstractmethod

from metricheq.core.connectors.base import Connector
from metricheq.evaluation.metric import Metric


class Deducer(ABC):
    def __init__(self, connector: Connector, params: dict):
        self.connector = connector
        self.client = connector.client
        self.params = params

    @abstractmethod
    def retrieve_data(self):
        pass

    @abstractmethod
    def process_data(self, data):
        pass

    @abstractmethod
    def finalize(self, processed_data):
        pass

    def deduce(self):
        self.connector.ensure_connectivity()
        data = self.retrieve_data()
        processed_data = self.process_data(data)
        return self.finalize(processed_data)

    @property
    def metric(self):
        return Metric(value=self.deduce())

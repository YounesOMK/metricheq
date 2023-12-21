from abc import ABC, abstractmethod

from metricheq.connectors.base import Connector


class Extractor(ABC):
    def __init__(self, connector: Connector, params: dict):
        self.connector = connector
        self.client = connector.client
        self.params = params

    @abstractmethod
    def friendly_name(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def process_data(self, data):
        pass

    @abstractmethod
    def finalize(self, processed_data):
        pass

    def perform(self):
        self.connector.ensure_connectivity()
        data = self.fetch_data()
        processed_data = self.process_data(data)
        return self.finalize(processed_data)

    def __str__(self):
        return self.friendly_name

from abc import ABC, abstractmethod
from .connections import BaseConnection


class BaseEndpoint(ABC):
    """
    This forces all endpoint objects to have a connection method and an
    endpoint attribute.
    """
    @abstractmethod
    def __init__(self, connection, endpoint):
        self.connection = connection
        self.endpoint = endpoint
        if not isinstance(self.connection, BaseConnection):
            raise TypeError('connection must be a BaseConnection object.')

from abc import ABC, abstractmethod


class BaseEndpoint(ABC):
    @abstractmethod
    def __init__(self, sync_emarsys):
        # This might look like a circular dependency, but it is not.
        # Here, the Emarsys class is used only to check that the
        # instantiated BaseEndpoint object is bound to an already existent
        # Emarsys object. Otherwise, it would not be able to make calls
        # to the Emarys api. That is why this import is deferred.
        from .emarsys import Emarsys
        self.emarsys = sync_emarsys
        if not isinstance(self.emarsys, Emarsys):
            raise TypeError('emarsys must be an Emarsys object.')

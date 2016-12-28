from abc import ABC, abstractmethod


class BaseEndpoint(ABC):
    @abstractmethod
    def __init__(self, sync_emarsys):
        # This might look like a circular dependency, but it is not.
        # Here, the SyncEmarsys class is used only to check that the
        # instantiated BaseEndpoint object is bound to an already existent
        # SyncEmarsys object. Otherwise, it would not be able to make calls
        # to the Emarys api. That is why this import is deferred.
        from .sync_emarsys import SyncEmarsys
        self.sync_emarsys = sync_emarsys
        if not isinstance(self.sync_emarsys, SyncEmarsys):
            raise TypeError('sync_emarsys must be a SyncEmarsys object.')


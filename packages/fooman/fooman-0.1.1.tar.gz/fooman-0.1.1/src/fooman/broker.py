from abc import ABC, abstractmethod


class Broker(ABC):
    def __init__(self, *, connection=None, url=None, **parameters):
        ...

    @abstractmethod
    async def connect(self, connection_string: str):
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    async def produce(self):
        raise NotImplementedError

    @abstractmethod
    async def consume(self):
        raise NotImplementedError

    async def declare_queue(self, queue_name):
        """Declare a queue on this broker.  This method must be
        idempotent.
        """
        raise NotImplementedError

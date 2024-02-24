from typing import Any

from .types import BrokerTypes
from .broker import Broker
from .brokers import RedisBroker, RabbitmqBroker
from .models import Request
from dataclasses import dataclass
import uuid
import json


class RpcClient:
    def __init__(
        self,
        client_name: str,
        connection_string: str,
        broker_type: str | BrokerTypes = BrokerTypes.REDIS,
        *args: list[Any],
        **kwargs: dict[str, Any],
    ):
        self._client_name = client_name
        self._broker_type = broker_type
        self._connection_string = connection_string

    async def call(self, method, service_name, params):
        await self._ensure_connection()
        correlation_id = uuid.uuid4().hex
        request = Request(
            method_name=method, arguments=params, correlation_id=correlation_id
        )
        await self.broker.produce(
            key=f"{service_name}.{method}", response=request.model_dump_json(), is_replay=False, correlation_id=correlation_id 
        )
        response = await self.broker.get_replay(key=f"{correlation_id}")
        response = json.loads(response.decode())
        return response["result"]

    async def _ensure_connection(self):
        self.broker = self._get_broker()
        await self.broker.connect(self._connection_string)

    def _get_broker(self) -> Broker:
        broker_map = {
            BrokerTypes.REDIS: RedisBroker,
            BrokerTypes.RABBITMQ: RabbitmqBroker
        }
        broker_type = self._broker_type
        broker_class = broker_map[
            BrokerTypes.from_string(broker_type)
            if not isinstance(broker_type, BrokerTypes)
            else broker_type
        ]
        return broker_class()

    def get(self, service_name):
        """
        TODO: Check if service_name actually exist!
        """
        return RpcService(name=service_name, client=self)


@dataclass
class RpcService:
    name: str
    client: RpcClient

    def __getattr__(self, method):
        async def wrap(*args, **kw):
            return await self.client.call(method, self.name, params=kw)

        return wrap

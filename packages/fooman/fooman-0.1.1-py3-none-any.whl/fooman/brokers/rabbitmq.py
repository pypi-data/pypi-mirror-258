from ..broker import Broker
from typing import Callable
import asyncio
import aio_pika
from aio_pika.abc import AbstractIncomingMessage


class RabbitmqBroker(Broker):
    futures = dict()
    result = None
    async def connect(self, connection_string, is_server=False, **kwargs):

        if getattr(self, "_connection", None):
            raise RuntimeError("Already started")

        self._connection = await aio_pika.connect_robust(connection_string)
        self._channel = await self._connection.channel()
        self._exchange = self._channel.default_exchange
        if is_server:
            self._callback_queue = await self._channel.declare_queue(kwargs["service_name"])
        else:
            self._callback_queue = await self._channel.declare_queue(exclusive=True)

    async def disconnect(self):
        connection = self._connection
        await connection.close()

    async def produce(self, key, response, is_replay=True, **kwargs):
        if is_replay:
            reply_to = kwargs["reply_to"]
            message = aio_pika.Message(
                            body=response.encode(),
                            correlation_id=key,
                        )
            await self._exchange.publish(
                        message,
                        routing_key=reply_to,
                    )
        else:
            loop = asyncio.get_running_loop()
            future = loop.create_future()
            correlation_id = kwargs["correlation_id"]
            self.futures[correlation_id] = future
            message = aio_pika.Message(
                    str(response).encode(),
                    content_type="text/plain",
                    correlation_id=correlation_id,
                    reply_to=self._callback_queue.name,
            )
            await self._exchange.publish(
                message,
                routing_key=key.split(".")[0]
            )

    async def on_response(self, message: AbstractIncomingMessage) -> None:
        if message.correlation_id is None:
            print(f"Bad message {message!r}")
            return

        future: asyncio.Future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def get_replay(self, key: str):
        await self._callback_queue.consume(self.on_response, no_ack=True)
        return await self.futures[key]

    async def consume(self, func: Callable, service_name, func_names, prefetch_count=1):
        async with self._callback_queue.iterator() as qiterator:
            message: aio_pika.abc.AbstractIncomingMessage
            async for message in qiterator:
                try:
                    async with message.process(requeue=False):
                        assert message.reply_to is not None
                        await func(message)
                except Exception:
                    print("Processing error for message %r", message)

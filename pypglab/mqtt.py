"""MQTT Client interface for pypglab."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any

# define a mqtt subscribe callback ... the input argument are payload and the topic string
Subcribe_CallBack = Callable[[str, str], None]

Sub_State = dict[str, Any]
Sub_States = dict[int, Sub_State]


class Client:
    """The client interface to mqtt."""

    def __init__(
        self,
        publish: Callable[
            [str, str, int | None, bool | None], Coroutine[Any, Any, dict]
        ],
        subscribe: Callable[
            [Sub_State, str, Subcribe_CallBack], Coroutine[Any, Any, dict]
        ],
        unsubscribe: Callable[[Sub_State], Coroutine[Any, Any, dict]],
    ) -> None:
        """Initialize."""

        self._publish = publish
        self._subscribe = subscribe
        self._unsubscribe = unsubscribe
        self._substates: Sub_States = {}

    async def publish(
        self, topic: str, payload: str, qos: int | None = 0, retain: bool | None = False
    ) -> None:
        """Publish a MQTT message."""
        if self._publish:
            await self._publish(topic, payload, qos, retain)

    async def subscribe(
        self, unique_id: int, topic: str, callback: Subcribe_CallBack
    ) -> None:
        """Subscribe to a MQTT topic."""

        if self._subscribe:
            # get the hash value from the topic
            hash_value = hash((unique_id, topic))

            # from all subribed topic states create/get one that match the hash
            substate = self._substates.get(hash_value)

            # call the mqtt client and get an substate update
            substate = await self._subscribe(substate, topic, callback)

            # save the sub state
            self._substates[hash_value] = substate

    async def unsubscribe(self, unique_id: int, topic: str) -> None:
        """Unsubscribe from a MQTT topics."""

        if self._unsubscribe:
            # get the substate from the topic
            hash_value = hash((unique_id, topic))
            substate = self._substates.get(hash_value)

            # call the mqtt client to unsubscribe
            substate = await self._unsubscribe(substate)

            # update the substate
            self._substates[hash_value] = substate

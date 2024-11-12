"""Relay for pypglab."""

from .const import ENTITY_RELAY, RELAY_STATE_OFF, RELAY_STATE_ON
from .entity import Entity
from .mqtt import Client


class Relay(Entity):
    """It's a PG LAB Electronics relay."""

    def __init__(
        self,
        device_id: str,
        device_name: str,
        index: int,
        mqtt: Client,
    ) -> None:
        """Initialize."""
        super().__init__(device_id, device_name, index, ENTITY_RELAY, mqtt)

        self._state: bool = None

    def status_change_received(self, payload: str) -> None:
        """Call o notify a new status change."""
        self._state = True if payload == RELAY_STATE_ON else False

    async def __set_state(self, state: bool) -> None:
        """Turn the relay on or off."""
        payload = RELAY_STATE_ON if state else RELAY_STATE_OFF
        await super().set_state(payload)

    async def turn_on(self) -> None:
        """Turn the relay on."""
        await self.__set_state(True)

    async def turn_off(self) -> None:
        """Turn the relay on."""
        await self.__set_state(False)

    @property
    def state(self) -> bool:
        """Get relay status."""
        return self._state


async def CreateRelay(
    device_id: str, device_name: str, index: int, mqtt: Client
) -> Relay:
    """Create and initialize a PG LAB relay instance."""

    relay = Relay(device_id, device_name, index, mqtt)
    return relay

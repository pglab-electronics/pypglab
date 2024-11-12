"""Shutter for pypglab."""

from .const import (
    ENTITY_SHUTTER,
    SHUTTER_CMD_CLOSE,
    SHUTTER_CMD_OPEN,
    SHUTTER_CMD_STOP,
    SHUTTER_STATE_CLOSED,
    SHUTTER_STATE_CLOSING,
    SHUTTER_STATE_OPEN,
    SHUTTER_STATE_OPENING,
)
from .entity import Entity
from .mqtt import Client


class Shutter(Entity):
    """It's a PG LAB Electronics shutter."""

    STATE_UNKNOWN = 0
    STATE_OPENING = 1
    STATE_OPEN = 2
    STATE_CLOSING = 3
    STATE_CLOSED = 4

    def __init__(
        self,
        device_id: str,
        device_name: str,
        index: int,
        mqtt: Client,
    ) -> None:
        """Initialize."""
        super().__init__(device_id, device_name, index, ENTITY_SHUTTER, mqtt)

        self._state = None

    def status_change_received(self, payload: str) -> None:
        """Call o notify a new status change."""
        if payload == SHUTTER_STATE_OPENING:
            self._state = Shutter.STATE_OPENING
        elif payload == SHUTTER_STATE_OPEN:
            self._state = Shutter.STATE_OPEN
        elif payload == SHUTTER_STATE_CLOSING:
            self._state = Shutter.STATE_CLOSING
        elif payload == SHUTTER_STATE_CLOSED:
            self._state = Shutter.STATE_CLOSED

    async def open(self) -> None:
        """Open the shutter."""
        await self.set_state(SHUTTER_CMD_OPEN)

    async def close(self) -> None:
        """Close the sutter."""
        await self.set_state(SHUTTER_CMD_CLOSE)

    async def stop(self) -> None:
        """Stop the shutter."""
        await self.set_state(SHUTTER_CMD_STOP)

    @property
    def state(self) -> int:
        """Get shutter status."""
        return self._state


async def CreateShutter(
    device_id: str, device_name: str, index: int, mqtt: Client
) -> Shutter:
    """Create and initialize a PG LAB shutter instance."""

    shutter = Shutter(device_id, device_name, index, mqtt)
    return shutter

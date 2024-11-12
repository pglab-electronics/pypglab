"""Sensor for pypglab."""

import json
from typing import Any, cast

from .const import ENTITY_SENSOR, SENSOR_REBOOT_TIME, SENSOR_TEMPERATURE, SENSOR_VOLTAGE
from .entity import Entity
from .mqtt import Client


def SensorDefaultValue(sensor_type: str) -> Any:
    """Return a default value for a sensor type."""
    if sensor_type == SENSOR_TEMPERATURE:
        return 0
    if sensor_type == SENSOR_VOLTAGE:
        return 0
    if sensor_type == SENSOR_REBOOT_TIME:
        return 0
    return None


def SensorValueCast(sensor_type: str, value: Any) -> Any:
    """Cast a value to the specific type of the sensor."""
    if sensor_type == SENSOR_TEMPERATURE:
        return cast(int, value)
    if sensor_type == SENSOR_VOLTAGE:
        return cast(int, value)    
    if sensor_type == SENSOR_REBOOT_TIME:
        return cast(int, value)
    return None


class Sensor(Entity):
    """It's a PG LAB Electronics sensor."""

    def __init__(
        self,
        device_id: str,
        device_name: str,
        config: [str],
        mqtt: Client,
    ) -> None:
        """Initialize."""
        super().__init__(device_id, device_name, 0, ENTITY_SENSOR, mqtt)

        # initialize all sensor value
        self._state: dict = {}
        for sensor_type in config:
            self._state[sensor_type] = SensorDefaultValue(sensor_type)

    def _getSensorValue(self, sensor_type: str, values: dict) -> Any:
        if sensor_type in values:
            return SensorValueCast(sensor_type, values[sensor_type])

        return None

    def status_change_received(self, payload: str) -> None:
        """Call to notify a new status change."""
        values = json.loads(payload)

        for s in self._state:
            newValue = self._getSensorValue(s, values)
            if newValue:
                self._state[s] = newValue

    @property
    def state(self) -> dict:
        """Get sensor status."""
        return self._state

    @property
    def size(self) -> int:
        """Return the number of stored sensor value."""
        return len(self._state)


async def CreateSensor(
    device_id: str, device_name: str, config: [str], mqtt: Client
) -> Sensor:
    """Create and initialize a PG LAB relay instance."""

    sensor = Sensor(device_id, device_name, config, mqtt)
    return sensor

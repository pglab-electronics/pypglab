"""A base class entity for pypglab."""

from collections.abc import Callable

from .const import ENTITY_SENSOR, ENTITY_TOPIC, TOPIC_PGLAB
from .mqtt import Client

State_Update = Callable[[str], None]


class Entity:
    """Base class for PG LAB entities."""

    # define a global id incremented for every instance
    entity_id: int = 0

    def __init__(
        self,
        device_id: str,
        device_name: str,
        entity_id: int,
        entity_type: str,
        mqtt: Client,
    ) -> None:
        """Initialize."""

        # device id connected to this entity
        self._device_id = device_id

        # device name connected to this entity
        self._device_name = device_name

        # entity id, usually a internal index
        self._id = entity_id

        # entity type
        self._type = entity_type

        # mqtt client interface
        self._mqtt = mqtt

        # external status update callback
        self._on_state_update_callback: State_Update = None

        # topic used for change entity status
        if entity_type is ENTITY_SENSOR:
            self._topic = f"{TOPIC_PGLAB}/{self._device_name}/{entity_type}/"
        else:
            self._topic = f"{TOPIC_PGLAB}/{self._device_name}/{entity_type}/{self._id}/"

        # entity hash, it's a uniquie entity identifier
        self._hash: int = hash(
            (Entity.entity_id, self._device_id, self._type, self._id)
        )

        # increment the global entity id
        Entity.entity_id = Entity.entity_id + 1

    def status_change_received(self, payload: str) -> None:
        """Call to notify a new status change.

        To be overwritten by child class.
        """

    def set_on_state_callback(self, on_state_update: State_Update) -> None:
        """Set a callback to inform about new state."""
        self._on_state_update_callback = on_state_update

    async def subscribe_topics(self) -> None:
        """PG LAB Entity subscribe to mqtt relay status changing."""

        def on_message(topic, payload) -> None:
            self.status_change_received(payload)

            if self._on_state_update_callback:
                self._on_state_update_callback(payload)

        set_cmd, state_cmd = ENTITY_TOPIC[self._type]
        status_update_topic = self._topic + state_cmd
        await self._mqtt.subscribe(self._hash, status_update_topic, on_message)

    async def unsubscribe_topics(self) -> None:
        """Unsubscribe from all MQTT topics."""

        set_cmd, state_cmd = ENTITY_TOPIC[self._type]
        status_update_topic = self._topic + state_cmd
        await self._mqtt.unsubscribe(self._hash, status_update_topic)

    async def set_state(self, payload: str) -> None:
        """Change the entity state."""
        set_cmd, state_cmd = ENTITY_TOPIC[self._type]
        # check if the entity allows to change status
        if set_cmd:
            topic = self._topic + set_cmd
            await self._mqtt.publish(topic, payload)

    @property
    def hash(self) -> int:
        """Return the entity unique id hash value."""
        return self._hash

    @property
    def id(self) -> int:
        """Get entity index id."""
        return self._id

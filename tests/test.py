
import unittest
import time
import json

from .mqtt import MQTT
from pypglab.device import Device
from pypglab.relay import Relay
from pypglab.shutter import Shutter
from pypglab.sensor import Sensor
from pypglab.const import SENSOR_TEMPERATURE

UNIT_TEST_CONNECTION_TIMEOUT = 10

# be sure that the PG LAB Electronics device shutter opening/closing time is less than the following time
UNIT_TEST_SHUTTER_OPEN_TIMEOUT  = 25
UNIT_TEST_SHUTTER_CLOSE_TIMEOUT  = 25

UNIT_TEST_SENSOR_TIMEOUT = 65

class TestPgLab(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self._mqtt = MQTT()
        self._mqtt.setup()
        self._mqtt.start()

    async def asyncTearDown(self):
        self._mqtt.stop()

    async def test_broker_connection(self):
        """Test MQTT Broker connection."""

        end_time = time.time() + UNIT_TEST_CONNECTION_TIMEOUT
        while time.time() < end_time:
            if self._mqtt.connected:
                break

        self.assertTrue(self._mqtt.connected, "No connection with MQTT broker.")

    async def _get_discovery(self):
        """Get the PG LAB MQTT discovery message."""
        discovery = None
        end_time = time.time() + UNIT_TEST_CONNECTION_TIMEOUT
        while time.time() < end_time:
            if self._mqtt.discovery:
                discovery = self._mqtt.discovery
                break

        self.assertTrue(len(discovery) > 0, "No PG LAB Electronics Devices are connected to the MQTT broker.")        
        return discovery
    
    async def _relay_toggle(self, r: Relay):
        state_update_changed : bool = False

        def state_changed(payload:str)->None:
            nonlocal state_update_changed
            state_update_changed = True
        
        r.set_on_state_callback(state_changed)

        # be sure that the relay is off
        await r.turn_off()
        time.sleep(1)

        await r.turn_on()
        time.sleep(1)
        self.assertTrue(r.state, "Unexpected relay state.")

        await r.turn_off()
        time.sleep(1)
        self.assertTrue( not r.state, "Unexpected relay state.")

        self.assertTrue(state_update_changed, "Relay Status update don't received.")


    async def _shutter_toggle(self, s: Shutter):
        state_update_changed : bool = False

        def state_changed(payload:str)->None:
            nonlocal state_update_changed
            state_update_changed = True
        
        s.set_on_state_callback(state_changed)

        # the test suppose that the shutter opening/closing time is 
        # bigger than 10 second

        # at this moment the state of the shutter is unknow
        # try to open the shutter for 2 seconds .. so we are sure that the shutter is not close
        await s.open()
        time.sleep(2)

        self.assertTrue( s.state is not Shutter.STATE_CLOSED, "Unexpected shutter state")

        # close the shutter and wait enough time to be sure the shutter is fully close
        await s.close()
        time.sleep(UNIT_TEST_SHUTTER_CLOSE_TIMEOUT)

        self.assertTrue( s.state is Shutter.STATE_CLOSED, "Unexpected shutter state")

        # we are sure that the shutte is fully close
        # open the shutter and check the state after 1 second
        await s.open()
        time.sleep(1)

        self.assertTrue( s.state is Shutter.STATE_OPENING, "Unexpected shutter state")

        # the shutter is opening ... stop and check the state
        await s.stop()
        time.sleep(1)
        self.assertTrue(s.state is Shutter.STATE_OPEN, "Unexpected shutter state")
        self.assertTrue(state_update_changed, "Shutter Status update don't received.")

    async def _sensor_state(self, sensor: Sensor):
            
        state_update_changed : bool = False

        def state_changed(payload:str)->None:
            nonlocal state_update_changed
            state_update_changed = True
        
        sensor.set_on_state_callback(state_changed)

        # wait for sensor update
        timeout = time.time() + UNIT_TEST_SENSOR_TIMEOUT
        while (not state_update_changed) and (time.time() < timeout):
            time.sleep(1)

        self.assertTrue(state_update_changed, "Sensor state update don't received.")
        self.assertTrue(sensor.state and len(sensor.state) > 0, "Sensor state unexpected state")

        # check if the cpu temperature value is been received... it should be available in every device
        self.assertTrue(sensor.state.get(SENSOR_TEMPERATURE), "Sensor Temperature not available")
        self.assertTrue(sensor.state.get(SENSOR_TEMPERATURE)>0, "Sensor Temperature unexpected value")

    async def _create_device(self, discovery) -> Device:
        pglab_device = Device()

        # get the discovery message
        discovery_topic, discovery_payload = discovery

        # decode the paylod from json
        discovery_payload = json.loads(discovery_payload)

        # try to configure the pglab_device
        bres = await pglab_device.config(self._mqtt.pglab_mqtt_client, discovery_payload, True)

        self.assertTrue( bres, "Error during PG LAB Electronics device configuration.")

        return pglab_device
    

    async def test_discovery(self):
        """Test if a PG LAB Electronics device is connected to the broker and publish the discovery message."""
        await self._get_discovery()

    async def test_device(self):
        """Test if it's possible to create a PG LAB Electronics device with the discovery message."""
        pglab_discovery = await self._get_discovery()

        for discovery in pglab_discovery:        
            pglab_device = await self._create_device(discovery)

            if pglab_device.is_eboard:
                self.assertTrue( len(pglab_device.relays) > 0 or len(pglab_device.shutters) > 0, "No shutters or relays available.")

    async def test_relay(self):
        """Test if change status on relay status change."""
        pglab_discovery = await self._get_discovery()

        for discovery in pglab_discovery:        
            pglab_device = await self._create_device(discovery)

            if len(pglab_device.relays) == 0:
                return
            
            for r in pglab_device.relays:
                await self._relay_toggle(r)


    async def test_shutter(self):
        """Test if change status on relay status change."""
        pglab_discovery = await self._get_discovery()

        for discovery in pglab_discovery:        
            pglab_device = await self._create_device(discovery)

            if len(pglab_device.shutters) == 0:
                return
            
            # test only one shutter because is going to take time
            shutter = pglab_device.shutters[0]
            await self._shutter_toggle(shutter)


    async def test_sensors(self):
        """Test device sensor value."""
        pglab_discovery = await self._get_discovery()

        for discovery in pglab_discovery:        
            pglab_device = await self._create_device(discovery)

            await self._sensor_state(pglab_device.sensors)
                

def suite():

    suite = unittest.TestSuite()
    suite.addTest(TestPgLab('test_broker_connection'))
    suite.addTest(TestPgLab('test_discovery'))
    suite.addTest(TestPgLab('test_device'))
    suite.addTest(TestPgLab('test_relay'))
    suite.addTest(TestPgLab('test_shutter'))
    suite.addTest(TestPgLab('test_sensors'))

    return suite


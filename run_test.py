import unittest
from tests.test import suite

# IMPORTANT !!!!! 
# Before to run the UnitTest:
#
# 1) Be sure that a MQTT broker is running and reachable from the unittest machine
#    Configure the USERNAME/PASSWORD in ./tests/mqtt.py
# 2) At least one PG LAB Electronics device must be connected to the MQTT broker
# 3) If the device is an E-Board be sure to have it configured to manage shutter and relay.
#    Be sure that the shutter opening/closing time is less thant the value 
#    UNIT_TEST_SHUTTER_OPEN_TIMEOUT  and  UNIT_TEST_SHUTTER_CLOSE_TIMEOUT  in ./tests/test.py

if __name__ == '__main__':

    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
from pyPgLab import *

def device_added(dev,code):
  print (dev," ",code)

pglab = pyPgLab()
print("version:",pglab.version())

pglab.cb_device_added.append(device_added)
pglab.start()
pglab.discover()

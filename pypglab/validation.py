"""PG LAB Electronics config validation."""
from __future__ import annotations
from typing import Any

import ipaddress
import re
import voluptuous as vol

from . const import PGLAB_DEVICE_TYPES, E_BOARD, E_RELAY, E_SWITCH, MANUFACTURER

def ipaddrs(value: Any)-> str:
    
    if value is None:
        raise vol.Invalid("IP address value is None.")        
    try:
        ipaddress.ip_address(value)
        return str(value)
    except ValueError:
        raise vol.Invalid("IP address is not valid.")
    

def macaddrs(value: Any)-> str:

    if value is None:
        raise vol.Invalid("MAC address value is None.")        

    result = re.match(r"([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}$",value)

    if result is None:
        raise vol.Invalid("MAC address is not valid.")        
    
    return str(value)

def devicetype(value: Any)-> str:

    if value is None:
        raise vol.Invalid("Device type value is None.")        

    if value == PGLAB_DEVICE_TYPES[E_BOARD]:
        return str(value)
    elif value == PGLAB_DEVICE_TYPES[E_RELAY]:
        return str(value)
    elif value == PGLAB_DEVICE_TYPES[E_SWITCH]:
        return str(value)

    raise vol.Invalid("Device type is not valid.")        
    
    return None

def version(value: Any)-> str:
    if value is None:
        raise vol.Invalid("Version Number is None.")
    
    result = re.match(r"^([0-9]+)\.([0-9]+)\.([0-9]+)?$",value)
    if result is None:
        raise vol.Invalid("Version Number is not valid.") 
    
    return str(value)

def manufacturer(value: Any)-> str:
    if value is None:
        raise vol.Invalid("Manufacturer string is None.")
    
    if value != MANUFACTURER:
        raise vol.Invalid("Unexpected Manufacturer string is not valid.") 
    return str(value)

def string(value: Any)-> str:
    if value is None:
        raise vol.Invalid("String value is None.")
    
    return str(value)


def shutter(value: Any)-> int:
    if value is None:
        raise vol.Invalid("Shutter number value is None.")

    if value < 0 or value > 32:
        raise vol.Invalid("Unexpected shutter numbers.")
    
    return int(value)

def boards(value:Any)-> str:
    if value is None:
        raise vol.Invalid("Boards connection string is None.")
    
    result = re.match(r"^[0-1]{8}$",value)
    if result is None:
        raise vol.Invalid("Invalid Boards connection string.") 

    return str(value)
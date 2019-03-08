#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygatt
from binascii import hexlify, unhexlify
import time

# Tool for debug PyGatt
#import logging
#logging.basicConfig()
#logging.getLogger('pygatt').setLevel(logging.DEBUG)

addrMACBLElist = ['7C:01:0A:7C:2E:76']
adapter = pygatt.GATTToolBackend()
uuidBLE = "0000ffe1-0000-1000-8000-00805f9b34fb"

def write(data, write_uuid):
    device.char_write(write_uuid, unhexlify(data))

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

while True:
    time.sleep(5)  # Délai avant de réveiller les module HM-10
    for addr in addrMACBLElist:  # Baylaye des module HM-10
        try:
            adapter.start()
            device = adapter.connect(addr)  # Connection to BLE
#            write(hexlify(str.encode("WAKEUP")), uuidBLE) # Réveillez le HM-10
            device.subscribe(uuidBLE, # Read data from BLE at any time
                     callback=handle_data)
            time.sleep(3)
        except:
            print("ça marche pas")
            adapter.stop()
        finally:
            adapter.stop()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygatt
from binascii import hexlify, unhexlify
import time
import json
import paho.mqtt.client as paho

# Tool for debug PyGatt
import logging
logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

bleDevices = {
  "mac": [
    "7C:01:0A:7C:2E:76",
    "7C:01:0A:7C:2E:76",
    "7C:01:0A:7C:2E:76",
  ],
  "nom": [
    "vincentcapteur",
    "vincenteffecteur",
    "MQTT Effecteur",
  ],
  "type": [
    "capteur",
    "effecteur",
    "effecteur",
  ],
  "topic": [
    "polytech/vincentcapteur",
    "polytech/vincenteffecteur",
    "home/lovelace/volet/set",
  ]
}

addrMACBLElist = ['7C:01:0A:7C:2E:76']
adapter = pygatt.GATTToolBackend()
uuidBLE = "0000ffe1-0000-1000-8000-00805f9b34fb"
broker="172.20.10.13"

def write(data, write_uuid, device):
    device.char_write(write_uuid, unhexlify(data))

def on_message(client, userdata, message):
    m_decode=str(message.payload.decode("utf-8","ignore"))
    print(m_decode)
    addr = bleDevices['mac'][bleDevices['topic'].index(message.topic)]
    print(addr)
    try:
        adapter.start()
        device = adapter.connect(addr)  # Connection to BLE
        print('m_decode')
        print(m_decode)
        if m_decode == "ON":
            print('1')
            device.char_write(uuidBLE, str.encode("1"))
        elif m_decode == "OFF":
            print('0')
            device.char_write(uuidBLE, str.encode("0"))
    except Exception as e:
        print('caca')
        logging.error(traceback.format_exc())

        adapter.stop()
    finally:
        adapter.stop()

client= paho.Client("client-002")
######Bind function to callback
client.on_message=on_message
#####
print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
for topic in bleDevices['topic']:
    print(topic)
    client.subscribe(topic)#subscribe

while True:
    time.sleep(5)  # Délai avant de réveiller les module HM-10


#
# def handle_data(handle, value):
#     """
#     handle -- integer, characteristic read handle the data was received on
#     value -- bytearray, the data returned in the notification
#     """
#     print("Received data: %s" % hexlify(value))
#
# while True:
#     time.sleep(5)  # Délai avant de réveiller les module HM-10
#     for addr in addrMACBLElist:  # Baylaye des module HM-10
#         try:
#             adapter.start()
#             device = adapter.connect(addr)  # Connection to BLE
# #            write(hexlify(str.encode("WAKEUP")), uuidBLE) # Réveillez le HM-10
#             device.subscribe(uuidBLE, # Read data from BLE at any time
#                      callback=handle_data)
#             time.sleep(3)
#         except:
#             print("ça marche pas")
#             adapter.stop()
#         finally:
#             adapter.stop()

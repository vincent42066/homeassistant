#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygatt
from binascii import hexlify, unhexlify
import time
import json
import paho.mqtt.client as paho

# Tool for debug PyGatt
# import logging
# logging.basicConfig()
# logging.getLogger('pygatt').setLevel(logging.DEBUG)

outfile = "/home/homeassistant/.homeassistant/ble_devices.json"
addrMACBLElist = ['7C:01:0A:7C:2E:76']
adapter = pygatt.GATTToolBackend()
uuidBLE = "0000ffe1-0000-1000-8000-00805f9b34fb"
broker="172.20.10.13"

with open(outfile, 'r') as json_file:
    bleDevices = json.load(json_file)

def on_message(client, userdata, message):
    """
    Cette fonction a pour but de recupérer les packet mqtt venant de home
    assistant pour les effecteur et d'envoyer la commande au module BLE.
    """
    m_decode=str(message.payload.decode("utf-8","ignore"))
    if bleDevices['type'][bleDevices['topic'].index(message.topic)] == "effecteur":
        # print(m_decode)
        addr = bleDevices['mac'][bleDevices['topic'].index(message.topic)]
        # print(addr)
        try:
            adapter.start()
            device = adapter.connect(addr)  # Connection to BLE
            if m_decode == "ON":
                # print('1')
                device.char_write(uuidBLE, str.encode("1"))
            elif m_decode == "OFF":
                # print('0')
                device.char_write(uuidBLE, str.encode("0"))
        except Exception as e:
            print('ca marche pas')
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


def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    # print("Received data: %s" % hexlify(value))
    mqttJson = {"unit": value.decode("utf-8","ignore")}
    print(mqttJson)
    data_out=json.dumps(mqttJson)
    client.publish(actualTopic, data_out)

while True:
    time.sleep(20)  # Délai avant de réveiller les modules HM-10
    with open(outfile, 'r') as json_file: # lecture du fichier json
        bleDevices = json.load(json_file)
        # print(bleDevices)
    for index in range(len(bleDevices['mac'])):  # Baylaye des modules HM-10
        if bleDevices['type'][index] == "capteur":
            actualTopic = bleDevices['topic'][index]
            try:
                adapter.start()
                device = adapter.connect(bleDevices['mac'][index])  # Connection to BLE
                device.subscribe(uuidBLE, # Read data from BLE at any time
                         callback=handle_data)
                time.sleep(3)
            except Exception as e:
                print('ça marche pas ')
            finally:
                adapter.stop()

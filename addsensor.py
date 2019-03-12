import time
import paho.mqtt.client as paho
import json
broker="172.20.10.13"
outfile = "/home/homeassistant/.homeassistant/ble_devices.json"
sensorFile = "/home/homeassistant/.homeassistant/sensors.yaml"
switchFile = "/home/homeassistant/.homeassistant/switch.yaml"
#define callback
def on_message(client, userdata, message):
    time.sleep(1)
    m_decode=str(message.payload.decode("utf-8","ignore"))
    dictMsg=json.loads(m_decode)
    dictMsg['topic'] = "polytech/" + dictMsg['nom'].replace(" ", "").lower()
    print(message.topic)
    if message.topic == "polytech/ajoutercapteur":
        dictMsg['type'] = "capteur"
        print(dictMsg)
        with open(sensorFile, "a") as myfile:
            myfile.write("\r\n- platform: mqtt\r\n  state_topic: \"" + dictMsg['topic'] + "\"\r\n  name: \"" + dictMsg['nom'] + "\"\r\n  value_template: '{{ value_json.unit }}'")
            myfile.close
    elif message.topic == "polytech/ajoutereffecteur":
        dictMsg['type'] = "effecteur"
        print(dictMsg)
        with open(switchFile, "a") as myfile:
            myfile.write("\r\n- platform: mqtt\r\n  command_topic: \"" + dictMsg['topic'] + "\"\r\n  name: \"" + dictMsg['nom']+ "\"\r\n")
            myfile.close
    with open(outfile, 'r') as json_file:
        print('coucou')
        dictFromFile = json.load(json_file)
        print(dictFromFile)
        for key in dictMsg.keys():
            dictFromFile[key].append(dictMsg[key])
        print(dictFromFile)
    with open(outfile, 'w') as json_file:
            json.dump(dictFromFile, json_file, indent=2)


client= paho.Client("client-001")
######Bind function to callback
client.on_message=on_message
#####
print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe("polytech/ajoutercapteur")#subscribe
client.subscribe("polytech/ajoutereffecteur")#subscribe
time.sleep(2)
# client.disconnect() #disconnect
# client.loop_stop() #stop loop
while True:
    time.sleep(10)

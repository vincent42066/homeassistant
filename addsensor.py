import time
import paho.mqtt.client as paho
import json
broker="172.20.10.13"
#define callback
def on_message(client, userdata, message):
    time.sleep(1)
    m_decode=str(message.payload.decode("utf-8","ignore"))
    dictMsg=json.loads(m_decode)
    dictMsg['topic'] = "polytech/" + dictMsg['nom'].replace(" ", "").lower()
    print(dictMsg)
    with open("sensors.yaml", "a") as myfile:
        myfile.write("\r\n- platform: mqtt\r\n  state_topic: " + dictMsg['topic'] + "\r\n  name: " + dictMsg['nom'] + "\r\n  value_template: '{{ value_json.unit }}'")
        myfile.close

client= paho.Client("client-001")
######Bind function to callback
client.on_message=on_message
#####
print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe("polytech/ajoutercapteur")#subscribe
time.sleep(2)
# client.disconnect() #disconnect
# client.loop_stop() #stop loop
while True:
    time.sleep(10)

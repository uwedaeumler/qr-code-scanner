import paho.mqtt.client as mqtt
import evdev
import sys
import os
import time
import json

#============================
# Constants and Parameters
#============================

MQTT_IP = 'localhost'
QR_CODE_TOPIC = 'qrcode' 
CONST_CAPS = 42
CONST_ENTER = 28
CONST_KEY_DOWN = 1
keys = "X^1234567890    qwertzuiop    asdfghjkl   : yxcvbnm )                                                                           "

#============================
# Help functions
#============================

# Callback function for connection to MQTT Client
def on_connect(client, userdata, flags, rc):
    print("Connected to " + MQTT_IP + " mqtt broker")

#============================
# Main Function
#============================

# Initialize MQTT Client
client = mqtt.Client()
# Add callback functions
client.on_connect = on_connect
# Connect to databus
client.connect(MQTT_IP)
client.loop_start()

# Get Scanner event and attach to event
qrdevice = evdev.InputDevice('/dev/input/event0')
barcode = ""
upper = 0

print ("INFO | Ready for scanning QR Codes")
sys.stdout.flush()

for event in qrdevice.read_loop():
    
    if (event.type == evdev.ecodes.EV_KEY) and (event.value == CONST_KEY_DOWN):
        keyvalue = keys[event.code]
        if event.code == CONST_CAPS: # Event.Code = Caps ==> Next value will be a capital letter
            upper = 1 
        else:
            if upper == 1: # Change letter to capitel letter 
                  keyvalue = keyvalue.upper()
                  upper = 0
            barcode += keyvalue
        
        # Check for QRCode end
        if event.code == CONST_ENTER:
            print(barcode)
            # Publish MQTT Topic and flush to logs
            client.publish(QR_CODE_TOPIC, barcode)
            sys.stdout.flush()
            barcode = ""

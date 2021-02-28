#!/usr/bin/python3
import socket
from wx import axtostr 
import aprslib
import json
import os
import math
import time
try:
    from .emitter import Client
except ImportError:
    from emitter import Client


AXUDP_IP = os.getenv('AXUDP_IP') or "0.0.0.0"
AXUDP_PORT = int(os.getenv('AXUDP_PORT') or 1234)
AXUDP_MODE = os.getenv('AXUDP_MODE') or "FM"


MQTT_SERVER = os.getenv('MQTT_SERVER') or "buildserver.hamfog.net"
MQTT_PORT = int(os.getenv('MQTT_PORT') or "44004")
MQTT_KEY = os.getenv('MQTT_KEY') or ""
MQTT_TOPIC = os.getenv('MQTT_TOPIC') or "aprs"

RECV_BUFFER_LENGTH=1500

axudpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
axudpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

axudpsocket.bind((AXUDP_IP, AXUDP_PORT))

emitter = Client()

emitter.connect(host=MQTT_SERVER, port=MQTT_PORT, secure=False)

connected = False

emitter.on_connect = lambda: print("Connected\n\n"); connected = True
emitter.on_disconnect = lambda: print("Disconnected\n\n")
emitter.on_presence = lambda p: print("Presence message on channel: '" + str(p) + "'\n\n")
emitter.on_message = lambda m: print("Message received on default handler, destined to " + m.channel + ": " + m.as_string() + "\n\n")
emitter.on_error = lambda e: print("Error received: " + str(e) + "\n\n")
emitter.on_me = lambda me: print("Information about Me received: " + str(me) + "\n\n")
emitter.on_keyban = lambda kb: print("Keyban message received: " + str(kb) + "\n\n")
emitter.loop_start()


while True:
    data, addr = axudpsocket.recvfrom(RECV_BUFFER_LENGTH)

    isaprs, metadata = axtostr(data)
    metadata = {k: int(v) for k, v in metadata.items()}
    try:
        aprsdict = aprslib.parse(isaprs)
        aprsdict.update(metadata)
        aprsdict.mode = AXUDP_MODE
        aprsjson = json.dumps(aprsdict)

        if connected:
            if "latitude" in aprsdict and "longitude" in aprsdict:
                emitter.publish(MQTT_KEY, f'/{MQTT_TOPIC}/point/{math.floor(aprsdict["latitude"])}/{math.floor(aprsdict["longitude"])}/{aprsdict["from"]}', aprsjson, {})
            
            emitter.publish(MQTT_KEY, f'{MQTT_TOPIC}/message/{aprsdict["from"]}', aprsjson, {})
    except (aprslib.ParseError, aprslib.UnknownFormat) as exp:
        print("Error parsing Packet:"+str(isaprs), exp)


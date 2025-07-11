import socket
import time
import json
from OSC import OSCClient, OSCMessage

# MDCX Configuration
MDCX_HOST = "127.0.0.1"
MDCX_OSC_PORT = 7475

# HTTP TCP Configuration
HTTP_HOST = "10.113.231.87"
HTTP_PORT = 8080

# Funktion zum Senden eines OSC-Kommandos
def oscsender(obj, topic, msg=None):
    try:
        if msg is None:
            obj.send(OSCMessage(topic))
            print("OSC LOG: TOPIC(" + str(topic) + ")")
        else:
            obj.send(OSCMessage(topic, msg))
            print("OSC LOG: TOPIC(" + str(topic) + ") MSG(" + str(msg) + ")")
    except Exception as e:
        print("OSC ERROR - failed to send!", e)

# OSC-Client für MDC-X Show Control
mdcx_osc = OSCClient()
mdcx_osc.connect((MDCX_HOST, MDCX_OSC_PORT))

# HTTP-Server-Socket starten
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HTTP_HOST, HTTP_PORT))
server_socket.listen(1)

print("Server gestartet. Warte auf Verbindung...")

while True:
    conn, addr = server_socket.accept()
    print("Verbunden mit:", addr)

    data = conn.recv(1024)
    if not data:
        break

    try:
        # JSON-Nachricht vom Client auslesen
        message = data.decode('utf-8')
        jsonmessage = json.loads(message)
        print("Empfangene Szene-Daten:", message)

        wagon1_scene = (jsonmessage.get("videoId1", 1)*2)-1 # default value 1
        wagon2_scene = jsonmessage.get("videoId2", 1)*2 # default value 1

        # OSC-Themenpfade erzeugen
        topic1 = "/mdc_layer1_preset" + str(wagon1_scene)
        topic2 = "/mdc_layer1_preset" + str(wagon2_scene)

        # Wiederhole die Abfolge 2-mal: Szene 1 -> Szene 2 -> Szene 1 -> Szene 2
        for i in range(4):
            print("Szene " + topic1)
            oscsender(mdcx_osc, topic1, 1.0)
            time.sleep(3)

            print("Szene "+ topic2)
            oscsender(mdcx_osc, topic2, 1.0)
            time.sleep(3)

        # Rückmeldung an den Client
        reply = "Szenen abgespielt"
        conn.sendall(reply.encode('utf-8'))

    except json.JSONDecodeError:
        error_msg = "Ungültiges JSON erhalten."
        print(error_msg)
        conn.sendall(error_msg.encode('utf-8'))

    conn.close()

import socket
import json
import sys

# Regeln basierend auf der Tabelle
# SCENE_RULES = [
#     (0, 10, 0, 10, "L5", "R5"),
#     (11, 20, 0, 10, "L7", "R3"),
#     (21, 30, 0, 10, "L7", "R2"),
#     (31, 40, 0, 10, "L8", "R2"),
#     (41, 1000, 0, 10, "L8", "R1"),
#     (0, 10, 11, 20, "L3", "R7"),
#     (11, 20, 11, 20, "L5", "R5"),
#     (21, 30, 11, 20, "L6", "R4"),
#     (31, 40, 11, 20, "L7", "R3"),
#     (41, 1000, 11, 20, "L7", "R3"),
#     (0, 10, 21, 30, "L2", "R7"),
#     (11, 20, 21, 30, "L4", "R6"),
#     (21, 30, 21, 30, "L5", "R5"),
#     (31, 40, 21, 30, "L6", "R4"),
#     (41, 1000, 21, 30, "L6", "R4"),
#     (0, 10, 31, 40, "L2", "R8"),
#     (11, 20, 31, 40, "L3", "R7"),
#     (21, 30, 31, 40, "L4", "R6"),
#     (31, 40, 31, 40, "L5", "R5"),
#     (41, 1000, 31, 40, "L6", "R4"),
#     (0, 10, 41, 1000, "L1", "R8"),
#     (11, 20, 41, 1000, "L3", "R7"),
#     (21, 30, 41, 1000, "L4", "R6"),
#     (31, 40, 41, 1000, "L4", "R6"),
#     (41, 1000, 41, 1000, "L5", "R5"),
# ]

# def find_scene(w1_count, w2_count):
#     for rule in SCENE_RULES:
#         min_w1, max_w1, min_w2, max_w2, vid1, vid2 = rule
#         if min_w1 <= w1_count <= max_w1 and min_w2 <= w2_count <= max_w2:
#             return f"V1{vid1}", f"V2{vid2}"
#     return "V1L0", "V2R0"  # Fallback-Szene bei keiner Übereinstimmung

def main():
    HOST = '127.0.0.1'  # IP-Adresse des Servers
    PORT = 8080         # Port des Servers

    # Passagierdaten eingeben (kann später automatisiert werden)
    # w1 = int(input("Anzahl Passagiere in Waggon 1: "))
    # w2 = int(input("Anzahl Passagiere in Waggon 2: "))

    # scene1, scene2 = find_scene(w1, w2)
    
    # Szenen als JSON vorbereiten
    # message = {
    #     "wagon1": scene1,
    #     "wagon2": scene2
    # }
    message = sys.argv[1]
    print(f"received data: {message}",file=sys.stderr, flush=True)
    json_message = json.loads(message)
    #json_message = message
    print(f"Sende folgende Szenen an den Server: {message}",file=sys.stderr, flush=True)

    # Verbindung aufbauen und JSON senden
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(message.encode('utf-8'))

    # Antwort vom Server empfangen
    data = client_socket.recv(1024)
    print("Antwort vom Server:", data.decode('utf-8'),file=sys.stderr, flush=True)

    client_socket.close()

if __name__ == "__main__":
    main()

# Beispielausgabe bei Eingabe:
# Anzahl Passagiere in Waggon 1: 12
# Anzahl Passagiere in Waggon 2: 9
# Sende folgende Szenen an den Server: {"wagon1": "V1L7", "wagon2": "V2R3"}
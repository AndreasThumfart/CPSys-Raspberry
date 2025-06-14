import socket
import json
import sys


def main():
    HOST = '10.113.231.87'  # IP-Adresse des Servers
    PORT = 8080         # Port des Servers

    # Szenen als JSON vorbereiten
    message = sys.argv[1]
    #message = "{\"videoId1\":1,\"videoId2\":2}"
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

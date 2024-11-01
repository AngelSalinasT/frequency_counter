import socket
import json


# Clase base Nodo
class Nodo:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def conectar(self, host, port):
        """Establece una conexión con otro nodo."""
        try:
            self.socket.connect((host, port))
            print(f"Conectado a {host}:{port}")
        except Exception as e:
            print(f"Error al conectar con {host}:{port} - {e}")

    def enviar(self, data):
        """Envía datos codificados en JSON."""
        try:
            self.socket.sendall(json.dumps(data).encode('utf-8'))
        except Exception as e:
            print(f"Error al enviar datos: {e}")

    def recibir(self, buffer_size=4096):
        """Recibe datos y los decodifica desde JSON."""
        try:
            data = self.socket.recv(buffer_size)
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            print(f"Error al recibir datos: {e}")
            return None
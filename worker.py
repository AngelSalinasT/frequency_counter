from node import Nodo
from count import countt  # Se usa countt sin inicio y fin
import socket
import json

class Worker(Nodo):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

    def aceptar_conexion(self):
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Conectado al Slave en {addr}")
            texto = self.recibir_texto(conn)
            resultado = countt(texto)  # Llama a countt sin índices de inicio y fin
            self.enviar_resultado(conn, resultado)  # Envía resultado y luego cierra conn

    def recibir_texto(self, conn):
        try:
            data = conn.recv(4096).decode('utf-8')
            print("Texto recibido del Slave")
            return data
        except Exception as e:
            print(f"Error al recibir texto: {e}")
            return ""
        finally:
            conn.close()  # Cierra la conexión después de recibir

    def enviar_resultado(self, conn, resultado):
        """Envía el resultado parcial al Slave."""
        try:
            conn.sendall(json.dumps(resultado).encode('utf-8'))
            print("Resultado parcial enviado al Slave")
        except Exception as e:
            print(f"Error al enviar resultado: {e}")
        finally:
            conn.close()  # Cierra solo después de enviar
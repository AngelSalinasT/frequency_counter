import socket
import json
from split_text import splitt  # Usamos la función proporcionada para dividir texto
from count import countt  # Usamos la función proporcionada para contar palabras


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



# Ejemplo de inicialización y ejecución
#if __name__ == "__main__":
#    # Parámetros de ejemplo
#    master_host = 'localhost'
#    master_port = 5000
#    slaves = [('localhost', 6000), ('localhost', 6001)]
#    workers_slave_1 = [('localhost', 7000), ('localhost', 7001)]
#    workers_slave_2 = [('localhost', 7002), ('localhost', 7003)]
#    texto = "Aquí va el texto a procesar que se dividirá entre los nodos."#

#    # Inicializa el master
#    master = Master(master_host, master_port, slaves, texto)
#    master.distribuir_texto()
#    resultado_final = master.recibir_resultados()
#    print("Resultado final:", resultado_final)

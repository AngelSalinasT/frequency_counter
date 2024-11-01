from node import Nodo
from split_text import splitt  # Función para dividir el texto
import socket
import json

class Slave(Nodo):
    def __init__(self, host, port, workers, master_host, master_port):
            super().__init__(host, port)
            self.workers = workers
            self.master_host = master_host
            self.master_port = master_port
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.server_socket.listen()

    def aceptar_conexion_master(self):
        """Espera y recibe conexión del Master para recibir el texto a procesar."""
        conn, addr = self.server_socket.accept()
        print(f"Conectado al Master en {addr}")
        texto = self.recibir_texto(conn)  # Recibe texto del Master
        print(f"Texto recibido del Master: {texto}")
        if texto:
            resultados = self.distribuir_a_workers(texto)
            self.enviar_resultado_al_master(resultados)

    def recibir_texto(self, conn):
        """Recibe la porción de texto desde el Master."""
        try:
            data = conn.recv(4096).decode('utf-8')
            print("Texto recibido del Master")
            return data
        except Exception as e:
            print(f"Error al recibir texto del Master: {e}")
            return ""
        finally:
            conn.close()

    def distribuir_a_workers(self, texto):
        """Divide la porción de texto y la distribuye a los Workers."""
        partes = splitt(texto, 0, len(self.workers))
        resultados = []

        for i, (worker_host, worker_port) in enumerate(self.workers):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as worker_socket:
                    worker_socket.connect((worker_host, worker_port))
                    parte_texto = texto[partes[i][0]:partes[i][1]]
                    worker_socket.sendall(parte_texto.encode('utf-8'))

                    # Recibe resultado del Worker
                    resultado = worker_socket.recv(4096)
                    if resultado:
                        resultados.append(json.loads(resultado.decode('utf-8')))
                    print(f"Resultado recibido del Worker {worker_host}:{worker_port}")
            except Exception as e:
                print(f"Error al conectar con Worker {worker_host}:{worker_port} - {e}")

        return self.combinar_resultados(resultados)

    def enviar_resultado_al_master(self, resultados):
        """Envía el resultado combinado al Master."""
        try:
            resultado_final = self.combinar_resultados(resultados)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as master_socket:
                master_socket.connect((self.master_host, self.master_port))
                master_socket.sendall(json.dumps(resultado_final).encode('utf-8'))
                print("Resultado final enviado al Master")
        except Exception as e:
            print(f"Error al enviar resultado al Master: {e}")

    def combinar_resultados(self, resultados):
        """Combina los resultados parciales en un solo diccionario."""
        resultado_final = {}
        for resultado in resultados:
            if isinstance(resultado, dict):  # Asegurarse de que sea un diccionario
                for palabra, frecuencia in resultado.items():
                    resultado_final[palabra] = resultado_final.get(palabra, 0) + frecuencia
        return resultado_final

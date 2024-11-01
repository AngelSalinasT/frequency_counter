from node import Nodo
from split_text import splitt  # Función para dividir el texto
import socket
import json

class Master(Nodo):
    def __init__(self, host, port, slaves, texto):
        super().__init__(host, port)
        self.slaves = slaves
        self.texto = texto

    def distribuir_texto(self):
        """Divide el texto y distribuye cada parte a los Slaves."""
        partes = splitt(self.texto, 0, len(self.slaves))

        for i, (slave_host, slave_port) in enumerate(self.slaves):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as slave_socket:
                    slave_socket.connect((slave_host, slave_port))
                    parte_texto = self.texto[partes[i][0]:partes[i][1]]
                    slave_socket.sendall(parte_texto.encode('utf-8'))
                    print(f"Texto enviado al Slave {slave_host}:{slave_port}")
            except Exception as e:
                print(f"Error al conectar con Slave {slave_host}:{slave_port} - {e}")

    def recibir_resultados(self):
        """Recibe los resultados combinados de cada Slave."""
        resultados = []

        for slave_host, slave_port in self.slaves:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as slave_socket:
                    slave_socket.connect((slave_host, slave_port))
                    resultado = slave_socket.recv(4096)
                    if resultado:
                        resultados.append(json.loads(resultado.decode('utf-8')))
                    print(f"Resultado recibido del Slave {slave_host}:{slave_port}")
            except Exception as e:
                print(f"Error al recibir datos del Slave {slave_host}:{slave_port} - {e}")

        return self.combinar_resultados(resultados)
    
    def combinar_resultados(self, resultados):
        """Combina los resultados parciales en un solo diccionario."""
        resultado_final = {}
        for resultado in resultados:
            for palabra, frecuencia in resultado.items():
                resultado_final[palabra] = resultado_final.get(palabra, 0) + frecuencia
        return resultado_final

from split_text import splitt  # Usamos la función proporcionada para dividir texto
from node import Nodo 

# Clase Slave
class Slave(Nodo):
    def __init__(self, host, port, workers):
        super().__init__(host, port)
        self.workers = workers  # Lista de (host, port) de workers

    def recibir_texto(self):
        """Recibe la porción de texto desde el Master."""
        texto = self.recibir()
        print("Texto recibido del Master")
        self.distribuir_a_workers(texto)

    def distribuir_a_workers(self, texto):
        """Divide la parte del texto y distribuye a los Workers."""
        partes = splitt(texto, 0, len(self.workers))
        resultados = []
        for i, (worker_host, worker_port) in enumerate(self.workers):
            self.conectar(worker_host, worker_port)
            parte_texto = texto[partes[i][0]:partes[i][1]]
            self.enviar(parte_texto)
            resultado = self.recibir()
            if resultado:
                resultados.append(resultado)
            self.socket.close()
        self.enviar_resultados_al_master(resultados)

    def enviar_resultados_al_master(self, resultados):
        """Envía los resultados combinados al Master."""
        resultado_final = self.combinar_resultados(resultados)
        self.conectar(self.host, self.port)
        self.enviar(resultado_final)
        self.socket.close()

    def combinar_resultados(self, resultados):
        """Combina los resultados parciales en un solo diccionario."""
        resultado_final = {}
        for resultado in resultados:
            for palabra, frecuencia in resultado.items():
                resultado_final[palabra] = resultado_final.get(palabra, 0) + frecuencia
        return resultado_final
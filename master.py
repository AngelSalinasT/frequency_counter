from node import Nodo 
from split_text import splitt  # Usamos la función proporcionada para dividir texto

# Clase Master
class Master(Nodo):
    def __init__(self, host, port, slaves, texto):
        super().__init__(host, port)
        self.slaves = slaves  # Lista de (host, port) de slaves
        self.texto = texto

    def distribuir_texto(self):
        """Divide el texto en partes y distribuye a cada Slave."""
        partes = splitt(self.texto, 0, len(self.slaves))
        for i, (slave_host, slave_port) in enumerate(self.slaves):
            self.conectar(slave_host, slave_port)
            parte_texto = self.texto[partes[i][0]:partes[i][1]]
            self.enviar(parte_texto)
            self.socket.close()

    def recibir_resultados(self):
        """Recibe los resultados parciales de los Slaves y los combina."""
        resultados = []
        for slave_host, slave_port in self.slaves:
            self.conectar(slave_host, slave_port)
            resultado = self.recibir()
            if resultado:
                resultados.append(resultado)
            self.socket.close()
        return self.combinar_resultados(resultados)

    def combinar_resultados(self, resultados):
        """Combina los resultados parciales en un solo diccionario."""
        resultado_final = {}
        for resultado in resultados:
            for palabra, frecuencia in resultado.items():
                resultado_final[palabra] = resultado_final.get(palabra, 0) + frecuencia
        return resultado_final

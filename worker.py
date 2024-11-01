from node import Nodo 
from split_text import splitt  # Usamos la función proporcionada para dividir texto
from count import countt

# Clase Worker
class Worker(Nodo):
    def __init__(self, host, port):
        super().__init__(host, port)

    def procesar_texto(self):
        """Recibe el texto desde el Slave, cuenta palabras y envía el resultado."""
        texto = self.recibir()
        print("Texto recibido del Slave")
        resultado = countt(texto)
        self.enviar(resultado)


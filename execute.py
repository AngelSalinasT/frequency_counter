from threading import Thread
from master import Master
from slave import Slave
from worker import Worker

def iniciar_slave(host, port, workers, master_host, master_port):
    """Inicia un hilo de Slave que escucha conexiones y conoce la dirección del Master."""
    slave = Slave(host, port, workers, master_host, master_port)
    slave.aceptar_conexion_master()  # Inicia el Slave para recibir del Master

def iniciar_worker(host, port):
    """Inicia un hilo de Worker que escucha conexiones."""
    worker = Worker(host, port)
    worker.aceptar_conexion()  # Inicia el Worker para recibir del Slave

if __name__ == "__main__":
    # Parámetros de configuración con puertos menos comunes
    master_host = 'localhost'
    master_port = 8500
    texto = "El perro corre rápidamente por el parque mientras los niños juegan con una pelota. El sol brilla y el aire es fresco, lo que hace que el día sea perfecto para jugar al aire libre."

    # Definir los Slaves y sus Workers con puertos poco comunes
    slaves = [('localhost', 8600), ('localhost', 8601)]
    workers_slave_1 = [('localhost', 8700), ('localhost', 8701)]
    workers_slave_2 = [('localhost', 8702), ('localhost', 8703)]

    # Iniciar los hilos de los Workers
    workers_threads = []
    for worker_host, worker_port in workers_slave_1 + workers_slave_2:
        t = Thread(target=iniciar_worker, args=(worker_host, worker_port))
        t.start()
        workers_threads.append(t)

    # Iniciar los hilos de los Slaves y pasarles la dirección del Master
    slaves_threads = []
    slave_configs = [
        (slaves[0][0], slaves[0][1], workers_slave_1, master_host, master_port),
        (slaves[1][0], slaves[1][1], workers_slave_2, master_host, master_port)
    ]
    for slave_host, slave_port, slave_workers, master_host, master_port in slave_configs:
        t = Thread(target=iniciar_slave, args=(slave_host, slave_port, slave_workers, master_host, master_port))
        t.start()
        slaves_threads.append(t)

    # Iniciar el Master en el hilo principal
    master = Master(master_host, master_port, slaves, texto)
    master.distribuir_texto()
    resultado_final = master.recibir_resultados()
    print("Resultado final:", resultado_final)

    # Esperar a que todos los hilos de Slaves y Workers terminen (opcional)
    for t in workers_threads + slaves_threads:
        t.join()

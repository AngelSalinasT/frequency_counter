from multiprocessing import Process
from master import Master
from slave import Slave
from worker import Worker

def iniciar_slave(host, port, workers):
    """Inicia un proceso de Slave que escucha conexiones."""
    slave = Slave(host, port, workers)
    slave.aceptar_conexion_master()  # Inicia el Slave para recibir del Master

def iniciar_worker(host, port):
    """Inicia un proceso de Worker que escucha conexiones."""
    worker = Worker(host, port)
    worker.aceptar_conexion()  # Inicia el Worker para recibir del Slave

if __name__ == "__main__":
    # Parámetros de configuración con puertos menos comunes
    master_host = 'localhost'
    master_port = 8500
    texto = "Aquí va el texto a procesar que se dividirá entre los nodos en diferentes puertos."

    # Definir los Slaves y sus Workers con puertos poco comunes
    slaves = [('localhost', 8600), ('localhost', 8601)]
    workers_slave_1 = [('localhost', 8700), ('localhost', 8701)]
    workers_slave_2 = [('localhost', 8702), ('localhost', 8703)]

    # Iniciar los procesos de los Workers
    workers_processes = []
    for worker_host, worker_port in workers_slave_1 + workers_slave_2:
        p = Process(target=iniciar_worker, args=(worker_host, worker_port))
        p.start()
        workers_processes.append(p)

    # Iniciar los procesos de los Slaves
    slaves_processes = []
    slave_configs = [(slaves[0][0], slaves[0][1], workers_slave_1), (slaves[1][0], slaves[1][1], workers_slave_2)]
    for slave_host, slave_port, slave_workers in slave_configs:
        p = Process(target=iniciar_slave, args=(slave_host, slave_port, slave_workers))
        p.start()
        slaves_processes.append(p)

    # Iniciar el Master en el proceso principal
    master = Master(master_host, master_port, slaves, texto)
    master.distribuir_texto()
    resultado_final = master.recibir_resultados()
    print("Resultado final:", resultado_final)

    # Esperar a que todos los procesos de Slaves y Workers terminen (opcional)
    for p in workers_processes + slaves_processes:
        p.join()

import multiprocessing
import random
import time

def generacion_binario():
    return bin(random.randint(0, 300))

def memoria():
    memoria = {}
    while len(memoria) < 50:
        pos = f"0x{random.randint(10, 99):02X}"
        memoria[pos] = " "  
    return memoria

def dispositivo(id, tipo, memoria, semaforo):
    print(f"[Dispositivo {id}] Intentando acceder al bus...")

    acquired = semaforo.acquire(timeout=0.1)
    if not acquired:
        print(f"[Dispositivo {id}] BUS OCUPADO. Esperando turno...")
        semaforo.acquire()

    print(f"[Dispositivo {id}] Accedió al bus. [{tipo.upper()}]")

    time.sleep(1) 

    if tipo == "escritura":
        for direccion in memoria.keys():
            if memoria[direccion] == " ":
                dato = generacion_binario()
                memoria[direccion] = dato
                print(f"[Dispositivo {id}] ESCRIBIÓ {dato} en {direccion}")
                break
    elif tipo == "lectura":
        direccion = random.choice(list(memoria.keys()))
        valor = memoria.get(direccion)
        if valor == " ":
            print(f"[Dispositivo {id}] LEYÓ {direccion} => VACÍO")
        else:
            print(f"[Dispositivo {id}] LEYÓ {direccion} => {valor}")

    time.sleep(random.uniform(0.5, 1.0))  

    print(f"[Dispositivo {id}] LIBERANDO el bus.\n")
    semaforo.release()

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    memoria_asignada = manager.dict(memoria())  
    semaforo_bus = multiprocessing.Semaphore(1)   

    procesos = []
    for i in range(10):  
        tipo = random.choice(["lectura", "escritura"])
        p = multiprocessing.Process(target=dispositivo, args=(i, tipo, memoria_asignada, semaforo_bus))
        procesos.append(p)

    print(" Iniciando simulación del bus...\n")
    for p in procesos:
        p.start()
    for p in procesos:
        p.join()

    print("\n Estado final de la memoria:")
    print(memoria_asignada)

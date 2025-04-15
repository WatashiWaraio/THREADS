# Sistemas Operativos 


## 🧠 Simulacion de bus 

Este proyecto tiene como objetivo simular un bus de datos compartido utilizando el módulo multiprocessing de Python. Se trata de un ejercicio práctico para entender cómo múltiples procesos pueden comunicarse y sincronizar el acceso a un recurso común en este caso, un "bus de datos".

Este código simula el comportamiento de un bus compartido, como los que existen en computadoras reales, donde varios dispositivos intentan acceder a una memoria central a través de un canal común de comunicación. Usamos multiprocessing para representar a cada dispositivo como un proceso separado que compite por el acceso a ese bus.


## 🧩 Comparación entre hardware real y esta simulación

| 💻 Concepto Real en SO                        | 🧪 Simulación en el Código Python                                      |
|---------------------------------------------|------------------------------------------------------------------------|
| Dispositivo físico (CPU, disco, DMA, etc.)  | `multiprocessing.Process` (cada proceso es un "dispositivo")          |
| Bus de datos compartido                     | `multiprocessing.Semaphore(1)` (controla acceso exclusivo)            |
| Arbitraje para acceso exclusivo             | `semaforo.acquire()` y `semaforo.release()`                           |
| Operación de lectura o escritura            | `dispositivo(id, tipo, memoria, semaforo)`                            |
| Memoria central compartida entre procesos   | `multiprocessing.Manager().dict()`                                    |
| Sincronización de acceso                    | `sleep()` simula tiempo de uso del bus y evita colisiones simultáneas |

---

## 🔬 Fundamento teórico (extraído del documento EC10)

### 1. ¿Qué es un bus?

Un **bus** es un conjunto de líneas de comunicación compartidas entre múltiples componentes (CPU, memoria, E/S). Su función es **transportar datos, direcciones y señales de control**.

- **Master**: unidad que inicia la comunicación (ej. CPU, DMA).
- **Slave**: unidad que responde a la petición (ej. memoria).

📌 En este código, todos los procesos hacen de master, y la memoria compartida es el único slave.

---

### 2. Protocolos de arbitraje

Cuando varios dispositivos intentan usar el bus al mismo tiempo, se necesita un **mecanismo de arbitraje**:

- **Centralizado** (como un árbitro): nuestro código simula esto con un `Semaphore(1)`.
- **Distribuido**: no lo implementamos aquí, pero se podría hacer con prioridades locales.

📍 El semáforo asegura que **solo un dispositivo tenga control del bus a la vez**, tal como lo hace el árbitro en un sistema real (protocolo tipo daisy-chaining o polling).

---

### 3. Tipos de transferencia

Aunque el código actual no distingue explícitamente entre protocolos **síncronos**, **asíncronos** o **semisíncronos**, el uso de `sleep()` para simular el retardo, y `acquire()` para esperar que el bus esté libre, refleja una forma de **protocolo semisíncrono** (sección 2.3 del documento).

---

## ⚙️ Código explicado por bloques

### `generacion_binario()`

Simula la creación de un dato aleatorio binario. En un entorno real sería el contenido a transferir.

---

### `memoria()`

Crea una "memoria" compartida de 50 direcciones vacías (tipo `0xAB`). Equivale a una tabla de memoria RAM en arquitectura real.

---

### `dispositivo(id, tipo, memoria, semaforo)`

Esta función representa un **proceso que intenta usar el bus**. El acceso al recurso está protegido por un semáforo que simula el arbitraje.

Pasos:

1. El proceso solicita el bus (`semaforo.acquire()`).
2. Si está ocupado, espera.
3. Simula uso del bus (`time.sleep()`).
4. Si es de **escritura**, escribe un dato binario en una dirección libre.
5. Si es de **lectura**, lee una dirección aleatoria y muestra su contenido.
6. Libera el bus (`semaforo.release()`).

---

### Bloque principal `if __name__ == '__main__'`

- Crea la memoria compartida y el semáforo.
- Lanza 10 procesos aleatorios (lectores/escritores).
- Espera a que todos terminen.
- Muestra el estado final de la memoria.


## 🚀 Ejecución del programa

```bash
python Exercise2.py
```

Ejemplo de salida:

```
[Dispositivo 0] Intentando acceder al bus...
[Dispositivo 1] BUS OCUPADO. Esperando turno...
[Dispositivo 0] Accedió al bus. [ESCRITURA]
[Dispositivo 0] ESCRIBIÓ 0b1101101 en 0xA3
[Dispositivo 0] LIBERANDO el bus.
...
```

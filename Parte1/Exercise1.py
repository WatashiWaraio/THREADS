import threading
import time
import random
import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

# Variables compartidas y bloqueo
clima_actual = {}
registro_datos = []
lock = threading.Lock()

# ============ HILO 1: Simulación de datos climáticos ============
def simular_datos_climaticos():
    temperatura = 20.0  # temperatura base
    humedad = 50.0      # humedad base
    presion = 1013.0    # presión base

    while True:
        with lock:
            temperatura += random.uniform(-0.5, 0.5)
            humedad += random.uniform(-1, 1)
            presion += random.uniform(-0.3, 0.3)

            clima_actual['fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            clima_actual['temperatura'] = round(temperatura, 2)
            clima_actual['humedad'] = round(humedad, 2)
            clima_actual['presion'] = round(presion, 2)

            registro_datos.append(clima_actual.copy())

        time.sleep(1)

# ============ HILO 2: Guardar en CSV cada 5 segundos ============
def guardar_en_csv():
    with open("registro_climatico.csv", mode='w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Fecha", "Temperatura", "Humedad", "Presion"])

    while True:
        time.sleep(5)
        with lock:
            with open("registro_climatico.csv", mode='a', newline='') as archivo:
                escritor = csv.writer(archivo)
                for fila in registro_datos:
                    escritor.writerow([fila['fecha'], fila['temperatura'], fila['humedad'], fila['presion']])
                registro_datos.clear()

# ============ HILO 3: Interfaz Gráfica ============
class InterfazClima:
    def __init__(self, root):
        self.root = root
        self.root.title("Estación Meteorológica")
        self.root.geometry("800x600")

        # Etiquetas de texto
        self.label_info = ttk.Label(root, text="Esperando datos...", font=("Arial", 14))
        self.label_info.pack(pady=10)

        # Figura de Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        self.temperaturas = []
        self.tiempos = []

        self.actualizar_grafico()

    def actualizar_grafico(self):
        with lock:
            if 'fecha' in clima_actual:
                self.tiempos.append(clima_actual['fecha'])
                self.temperaturas.append(clima_actual['temperatura'])

                if len(self.tiempos) > 20:
                    self.tiempos = self.tiempos[-20:]
                    self.temperaturas = self.temperaturas[-20:]

                # Actualizar gráfica
                self.ax.clear()
                self.ax.plot(self.tiempos, self.temperaturas, label='Temperatura (°C)', color='red')
                self.ax.set_xlabel("Tiempo")
                self.ax.set_ylabel("Temperatura (°C)")
                self.ax.set_title("Temperatura en Tiempo Real")
                self.ax.tick_params(axis='x', rotation=45)
                self.ax.legend()
                self.fig.tight_layout()
                self.canvas.draw()

                # Descripción textual
                descripcion = (
                    f"Fecha/Hora: {clima_actual['fecha']}\n"
                    f"Temperatura: {clima_actual['temperatura']} °C\n"
                    f"Humedad: {clima_actual['humedad']} %\n"
                    f"Presión: {clima_actual['presion']} hPa"
                )
                self.label_info.config(text=descripcion)

        self.root.after(1000, self.actualizar_grafico)

# ============ Inicialización de Hilos ============
if __name__ == "__main__":
    hilo_datos = threading.Thread(target=simular_datos_climaticos, daemon=True)
    hilo_guardado = threading.Thread(target=guardar_en_csv, daemon=True)

    hilo_datos.start()
    hilo_guardado.start()

    # Iniciar interfaz
    root = tk.Tk()
    app = InterfazClima(root)
    root.mainloop()

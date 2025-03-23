import tkinter as tk
import threading
import time

# Importar funciones desde 'algorithms.py'
from algorithms import (
    bubble_sort,
    quick_sort,
    insertion_sort,
    busqueda_secuencial,
    busqueda_binaria,
    generar_arreglo_aleatorio
)

class CarreraAlgoritmos:
    def __init__(self, master):
        self.master = master
        self.master.title("Carrera de Algoritmos")

        self.btn_iniciar = tk.Button(master, text="Iniciar Carrera", command=self.iniciar_carrera)
        self.btn_iniciar.pack(pady=10)

        self.txt_resultados = tk.Text(master, width=130, height=115, state='disabled')
        self.txt_resultados.pack(pady=10)

        self.tiempos = {}
        self.algoritmos_terminados = 0

        self.lock = threading.Lock()

    def escribir_resultado(self, mensaje):
        """Escribe mensaje en el Text sin borrar lo anterior."""
        self.txt_resultados.config(state='normal')
        self.txt_resultados.insert(tk.END, mensaje + "\n")
        self.txt_resultados.config(state='disabled')
        self.txt_resultados.see(tk.END)

    def algoritmo_terminado(self, nombre_algoritmo, tiempo):
        """Se llama cuando cada algoritmo termina."""
        with self.lock:
            self.tiempos[nombre_algoritmo] = tiempo
            self.algoritmos_terminados += 1

            self.escribir_resultado(f"[{nombre_algoritmo}] terminó en {tiempo:.6f} segundos.")

            # Si ya terminaron todos, mostramos quién fue el más rápido
            if self.algoritmos_terminados == 5:
                # Ordenamos por tiempo
                ganador = min(self.tiempos, key=self.tiempos.get)
                self.escribir_resultado("-------------------------------------------------")
                self.escribir_resultado(f"¡El algoritmo más rápido fue: {ganador}!")
                self.btn_iniciar.config(state='normal')  # Reactivamos el botón

    def run_bubble_sort(self, arr_original):
        arr_copia = arr_original[:]
        start = time.perf_counter()
        bubble_sort(arr_copia)
        end = time.perf_counter()
        self.algoritmo_terminado("Bubble Sort", end - start)

    def run_quick_sort(self, arr_original):
        arr_copia = arr_original[:]
        start = time.perf_counter()
        quick_sort(arr_copia)
        end = time.perf_counter()
        self.algoritmo_terminado("Quick Sort", end - start)

    def run_insertion_sort(self, arr_original):
        arr_copia = arr_original[:]
        start = time.perf_counter()
        insertion_sort(arr_copia)
        end = time.perf_counter()
        self.algoritmo_terminado("Insertion Sort", end - start)

    def run_busqueda_secuencial(self, arr_original, valor):
        start = time.perf_counter()
        busqueda_secuencial(arr_original, valor)
        end = time.perf_counter()
        self.algoritmo_terminado("Búsqueda Secuencial", end - start)

    def run_busqueda_binaria(self, arr_original, valor):
        arr_ordenado = sorted(arr_original)
        start = time.perf_counter()
        busqueda_binaria(arr_ordenado, valor)
        end = time.perf_counter()
        self.algoritmo_terminado("Búsqueda Binaria", end - start)

    def iniciar_carrera(self):
        # Limpiamos el text y los datos de la carrera anterior
        self.txt_resultados.config(state='normal')
        self.txt_resultados.delete("1.0", tk.END)
        self.txt_resultados.config(state='disabled')

        self.tiempos.clear()
        self.algoritmos_terminados = 0

        # Desactivamos el botón mientras corre la carrera
        self.btn_iniciar.config(state='disabled')

        # Generamos un array aleatorio y un valor a buscar
        tamaño = 3000  # Ajusta para ver más o menos diferencia
        arr = generar_arreglo_aleatorio(tamaño, minimo=0, maximo=10000)
        valor_a_buscar = arr[len(arr)//2]  # Por ejemplo, elegimos un valor a la mitad

        self.escribir_resultado("Iniciando carrera de algoritmos...\n")
        self.escribir_resultado(f"Se generó un arreglo de {tamaño} elementos.")
        self.escribir_resultado(f"Valor a buscar: {valor_a_buscar}")
        self.escribir_resultado("-------------------------------------------------\n")

        # Creamos e iniciamos los threads
        t_bubble = threading.Thread(target=self.run_bubble_sort, args=(arr,))
        t_quick = threading.Thread(target=self.run_quick_sort, args=(arr,))
        t_insertion = threading.Thread(target=self.run_insertion_sort, args=(arr,))
        t_sec = threading.Thread(target=self.run_busqueda_secuencial, args=(arr, valor_a_buscar))
        t_bin = threading.Thread(target=self.run_busqueda_binaria, args=(arr, valor_a_buscar))

        t_bubble.start()
        t_quick.start()
        t_insertion.start()
        t_sec.start()
        t_bin.start()

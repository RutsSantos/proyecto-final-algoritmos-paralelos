import random
import time
import threading
import tkinter as tk
from tkinter import messagebox

def bubble_sort(arr):
    """Algoritmo de ordenamiento: Burbuja."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def quick_sort(arr):
    """Algoritmo de ordenamiento: Quick Sort."""
    def _quick_sort(sub_arr, low, high):
        if low < high:
            pivot_index = partition(sub_arr, low, high)
            _quick_sort(sub_arr, low, pivot_index - 1)
            _quick_sort(sub_arr, pivot_index + 1, high)

    def partition(sub_arr, low, high):
        pivot = sub_arr[high]
        i = low - 1
        for j in range(low, high):
            if sub_arr[j] <= pivot:
                i += 1
                sub_arr[i], sub_arr[j] = sub_arr[j], sub_arr[i]
        sub_arr[i+1], sub_arr[high] = sub_arr[high], sub_arr[i+1]
        return i + 1

    _quick_sort(arr, 0, len(arr) - 1)


def insertion_sort(arr):
    """Algoritmo de ordenamiento: Inserción."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def busqueda_secuencial(arr, valor):
    """Búsqueda Secuencial: retorna índice del valor o -1 si no se encuentra."""
    for i in range(len(arr)):
        if arr[i] == valor:
            return i
    return -1

def busqueda_binaria(arr, valor):
    """Búsqueda Binaria: requiere que arr ya esté ordenado. Retorna índice o -1."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == valor:
            return mid
        elif arr[mid] < valor:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# -------------------------------
# Clase principal de la aplicación
# -------------------------------

class CarreraAlgoritmos:
    def __init__(self, master):
        self.master = master
        self.master.title("Carrera de Algoritmos")

        # Botón para iniciar la carrera
        self.btn_iniciar = tk.Button(master, text="Iniciar Carrera", command=self.iniciar_carrera)
        self.btn_iniciar.pack(pady=10)

        # Área de texto donde se mostrarán los resultados
        self.txt_resultados = tk.Text(master, width=60, height=15, state='disabled')
        self.txt_resultados.pack(pady=10)

        # Diccionario para almacenar los tiempos de cada algoritmo
        self.tiempos = {}
        # Variable para saber cuántos algoritmos han terminado
        self.algoritmos_terminados = 0
        # Lock para escribir concurrentemente
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
        # Para la búsqueda binaria, necesitamos un array ordenado
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

        # Desactivamos el botón para evitar que el usuario reinicie la carrera
        self.btn_iniciar.config(state='disabled')

        # Generamos un array aleatorio y un valor a buscar
        tamaño = 3000  # Ajusta el tamaño para ver más o menos la diferencia
        arr = [random.randint(0, 10000) for _ in range(tamaño)]
        valor_a_buscar = random.choice(arr)

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

# -------------------------------
# Punto de entrada de la aplicación
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CarreraAlgoritmos(root)
    root.mainloop()

import random

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

def generar_arreglo_aleatorio(tamaño, minimo=0, maximo=10000):
    """Genera un arreglo aleatorio para pruebas."""
    return [random.randint(minimo, maximo) for _ in range(tamaño)]

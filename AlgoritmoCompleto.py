# Algoritmo de fuerza bruta 
import time
import random
import matplotlib.pyplot as plt
import numpy as np

# Algoritmo 1: Fuerza bruta (Theta(n^2))
def max_subarray_brute_force(arr):
    max_sum = float('-inf')
    for i in range(len(arr)):
        current_sum = 0
        for j in range(i, len(arr)):
            current_sum += arr[j]
            max_sum = max(max_sum, current_sum)
    return max_sum

# Algoritmo de Divide y vencerás 
# Algoritmo 2: Divide y vencerás (O(n log n))
def max_crossing_sum(arr, left, mid, right):
    left_sum = float('-inf')
    sum_val = 0
    for i in range(mid, left - 1, -1):
        sum_val += arr[i]
        left_sum = max(left_sum, sum_val)
    
    right_sum = float('-inf')
    sum_val = 0
    for i in range(mid + 1, right + 1):
        sum_val += arr[i]
        right_sum = max(right_sum, sum_val)
    
    return left_sum + right_sum

def max_subarray_divide_conquer(arr, left, right):
    if left == right:
        return arr[left]
    
    mid = (left + right) // 2
    left_max = max_subarray_divide_conquer(arr, left, mid)
    right_max = max_subarray_divide_conquer(arr, mid + 1, right)
    cross_max = max_crossing_sum(arr, left, mid, right)
    
    return max(left_max, right_max, cross_max)

# Algoritmo de Programación dinámica 
# Algoritmo de Programacion Dinamica(O(n))
def max_subarray_kadane(arr):
    max_sum = float('-inf')
    current_sum = 0
    for num in arr:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum



# Función para medir el tiempo de ejecución
def measure_time(algorithm, arr):
    start = time.time()
    result = algorithm(arr)
    end = time.time()
    return end - start, result


# Código Python del plan de ejecución 

# Generación de datos aleatorios
def generate_test_cases(size):
    return [random.randint(-100, 100) for _ in range(size)]

# Ejecución del experimento y análisis de tiempos
def run_experiment():
    sizes = [10, 50, 100, 500, 1000, 5000]
    algorithms = {
        "Brute Force": max_subarray_brute_force,
        "Divide & Conquer": lambda arr: max_subarray_divide_conquer(arr, 0, len(arr) - 1),
        "Kadane's Algorithm": max_subarray_kadane
    }
    
    results = {algo: [] for algo in algorithms.keys()}
    stats = {algo: {"mean": [], "median": [], "std": []} for algo in algorithms.keys()}
    
    for size in sizes:
        arr = generate_test_cases(size)
        for name, algo in algorithms.items():
            times = []
            for _ in range(5):  # Repetir 5 veces para reducir variabilidad
                start_time = time.time()
                algo(arr)
                end_time = time.time()
                times.append(end_time - start_time)
            
            mean_time = np.mean(times)
            median_time = np.median(times)
            std_time = np.std(times)
            
            results[name].append(mean_time)
            stats[name]["mean"].append(mean_time)
            stats[name]["median"].append(median_time)
            stats[name]["std"].append(std_time)



# Código Python para el análisis de resultados 
# Graficar resultados
    plt.figure(figsize=(10, 6))
    for name, times in results.items():
        plt.plot(sizes, times, marker='o', label=name)
    plt.xlabel("Tamaño del arreglo")
    plt.ylabel("Tiempo de ejecución (s)")
    plt.title("Comparación de algoritmos para suma máxima de subarreglo")
    plt.legend()
    plt.xscale("log")
    plt.yscale("log")
    plt.grid()
    plt.show()
    
    # Imprimir estadísticas
    for name, data in stats.items():
        print(f"\n{name}:")
        for i, size in enumerate(sizes):
            print(f"Tamaño {size}: Media = {data['mean'][i]:.6f}, Mediana = {data['median'][i]:.6f}, Desviación estándar = {data['std'][i]:.6f}")

# Ejecutar el experimento
run_experiment()

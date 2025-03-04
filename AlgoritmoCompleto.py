import time
import random
import matplotlib.pyplot as plt
import numpy as np
import memory_profiler
import csv

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

# Tiempo de ejecución
def max_subarray_n2(arr):
    n = len(arr)
    max_sum = float('-inf')
    operations = 0
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            operations += 1
            max_sum = max(max_sum, current_sum)
    return max_sum, operations

def max_subarray_divide_and_conquer(arr, left, right, operations):
    if left == right:
        return arr[left], operations + 1
    
    mid = (left + right) // 2
    left_max, operations = max_subarray_divide_and_conquer(arr, left, mid, operations)
    right_max, operations = max_subarray_divide_and_conquer(arr, mid + 1, right, operations)
    cross_max, operations = max_crossing_subarray(arr, left, mid, right, operations)
    
    return max(left_max, right_max, cross_max), operations

def max_crossing_subarray(arr, left, mid, right, operations):
    left_sum = float('-inf')
    sum_temp = 0
    for i in range(mid, left - 1, -1):
        sum_temp += arr[i]
        operations += 1
        left_sum = max(left_sum, sum_temp)
    
    right_sum = float('-inf')
    sum_temp = 0
    for i in range(mid + 1, right + 1):
        sum_temp += arr[i]
        operations += 1
        right_sum = max(right_sum, sum_temp)
    
    return left_sum + right_sum, operations

def max_subarray_n(arr):
    max_sum = current_sum = arr[0]
    operations = 1
    for num in arr[1:]:
        current_sum = max(num, current_sum + num)
        operations += 1
        max_sum = max(max_sum, current_sum)
    return max_sum, operations

def run_experiment():
    sizes = [10, 50, 100, 500, 1000, 5000]
    algorithms = {
        "Brute Force": max_subarray_brute_force,
        "Divide & Conquer": lambda arr: max_subarray_divide_conquer(arr, 0, len(arr) - 1),
        "Kadane's Algorithm": max_subarray_kadane
    }
    
    # Estructuras para almacenar resultados de tiempo
    results = {algo: [] for algo in algorithms.keys()}
    stats = {algo: {"mean": [], "median": [], "std": []} for algo in algorithms.keys()}
    
    # Resultados detallados para CSV
    csv_results = []
    
    for size in sizes:
        arr = [random.randint(-100, 100) for _ in range(size)]
        
        # Mediciones detalladas para cada algoritmo
        for name, algo in algorithms.items():
            # Mediciones de tiempo
            times = []
            for _ in range(5):  # Repetir 5 veces para reducir variabilidad
                start_time = time.perf_counter()
                algo(arr)
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            
            # Cálculo de estadísticas
            mean_time = np.mean(times)
            median_time = np.median(times)
            std_time = np.std(times)
            
            results[name].append(mean_time)
            stats[name]["mean"].append(mean_time)
            stats[name]["median"].append(median_time)
            stats[name]["std"].append(std_time)
        
        # Mediciones de memoria y operaciones
        mem_before = memory_profiler.memory_usage()[0]
        start_time = time.perf_counter()
        max_sum_n2, operations_n2 = max_subarray_n2(arr)
        end_time = time.perf_counter()
        mem_after = memory_profiler.memory_usage()[0]
        time_n2 = end_time - start_time
        mem_n2 = mem_after - mem_before
        
        mem_before = memory_profiler.memory_usage()[0]
        start_time = time.perf_counter()
        max_sum_dc, operations_dc = max_subarray_divide_and_conquer(arr, 0, len(arr) - 1, 0)
        end_time = time.perf_counter()
        mem_after = memory_profiler.memory_usage()[0]
        time_dc = end_time - start_time
        mem_dc = mem_after - mem_before
        
        mem_before = memory_profiler.memory_usage()[0]
        start_time = time.perf_counter()
        max_sum_n, operations_n = max_subarray_n(arr)
        end_time = time.perf_counter()
        mem_after = memory_profiler.memory_usage()[0]
        time_n = end_time - start_time
        mem_n = mem_after - mem_before
        
        # Guardar resultados detallados
        csv_results.append([
            size, 
            time_n2, operations_n2, mem_n2, 
            time_dc, operations_dc, mem_dc, 
            time_n, operations_n, mem_n
        ])
    
    # Graficar resultados de tiempo
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
    
    # Imprimir estadísticas de tiempo
    for name, data in stats.items():
        print(f"\n{name}:")
        for i, size in enumerate(sizes):
            print(f"Tamaño {size}: Media = {data['mean'][i]:.6f}, Mediana = {data['median'][i]:.6f}, Desviación estándar = {data['std'][i]:.6f}")
    
    # Guardar resultados detallados en CSV
    with open('experiment_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Size", "Time N2", "Ops N2", "Mem N2", "Time DC", "Ops DC", "Mem DC", "Time N", "Ops N", "Mem N"])
        writer.writerows(csv_results)

# Ejecutar el experimento
run_experiment()


import time
import random
import csv
import matplotlib.pyplot as plt

# Algoritmo O(n²)
def max_subarray_n2(arr):
    n = len(arr)
    max_sum = float('-inf')
    operations = 0  # Contador de operaciones
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            operations += 1  # Contar cada iteración
            max_sum = max(max_sum, current_sum)
    return max_sum, operations

# Algoritmo O(n log n)
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

# Algoritmo O(n)
def max_subarray_n(arr):
    max_sum = current_sum = arr[0]
    operations = 1
    for num in arr[1:]:
        current_sum = max(num, current_sum + num)
        operations += 1
        max_sum = max(max_sum, current_sum)
    return max_sum, operations

# Experimento
def run_experiment():
    sizes = [10, 100, 500, 1000, 5000]
    num_trials = 30
    results = {size: {'time_n2': [], 'time_dc': [], 'time_n': [], 'ops_n2': [], 'ops_dc': [], 'ops_n': []} for size in sizes}

    for size in sizes:
        for _ in range(num_trials):
            arr = [random.randint(-100, 100) for _ in range(size)]

            start_time = time.perf_counter()
            _, operations_n2 = max_subarray_n2(arr)
            end_time = time.perf_counter()
            results[size]['time_n2'].append(end_time - start_time)
            results[size]['ops_n2'].append(operations_n2)

            start_time = time.perf_counter()
            _, operations_dc = max_subarray_divide_and_conquer(arr, 0, len(arr) - 1, 0)
            end_time = time.perf_counter()
            results[size]['time_dc'].append(end_time - start_time)
            results[size]['ops_dc'].append(operations_dc)

            start_time = time.perf_counter()
            _, operations_n = max_subarray_n(arr)
            end_time = time.perf_counter()
            results[size]['time_n'].append(end_time - start_time)
            results[size]['ops_n'].append(operations_n)

    # Guardar resultados en CSV
    with open('experiment_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Size", "Avg Time N2", "Avg Ops N2", "Avg Time DC", "Avg Ops DC", "Avg Time N", "Avg Ops N"])
        for size in sizes:
            writer.writerow([
                size,
                sum(results[size]['time_n2']) / num_trials,
                sum(results[size]['ops_n2']) / num_trials,
                sum(results[size]['time_dc']) / num_trials,
                sum(results[size]['ops_dc']) / num_trials,
                sum(results[size]['time_n']) / num_trials,
                sum(results[size]['ops_n']) / num_trials
            ])

    plot_results(results, sizes)

# Gráficos
def plot_results(results, sizes):
    avg_time_n2 = [sum(results[size]['time_n2']) / len(results[size]['time_n2']) for size in sizes]
    avg_time_dc = [sum(results[size]['time_dc']) / len(results[size]['time_dc']) for size in sizes]
    avg_time_n = [sum(results[size]['time_n']) / len(results[size]['time_n']) for size in sizes]

    avg_ops_n2 = [sum(results[size]['ops_n2']) / len(results[size]['ops_n2']) for size in sizes]
    avg_ops_dc = [sum(results[size]['ops_dc']) / len(results[size]['ops_dc']) for size in sizes]
    avg_ops_n = [sum(results[size]['ops_n']) / len(results[size]['ops_n']) for size in sizes]

    # Imprimir cantidad de operaciones por algoritmo
    for i, size in enumerate(sizes):
        print(f"Size {size}: O(n²) -> {avg_ops_n2[i]:.2f} ops, O(n log n) -> {avg_ops_dc[i]:.2f} ops, O(n) -> {avg_ops_n[i]:.2f} ops")

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, avg_time_n2, marker='o', label='O(n²)', linestyle='dashed')
    plt.plot(sizes, avg_time_dc, marker='s', label='O(n log n)', linestyle='dotted')
    plt.plot(sizes, avg_time_n, marker='^', label='O(n)', linestyle='solid')

    plt.xlabel('Array Size')
    plt.ylabel('Average Execution Time (seconds)')
    plt.title('Algorithm Performance Comparison')
    plt.legend()
    plt.grid()
    plt.show()

# Ejecutar el experimento
run_experiment()


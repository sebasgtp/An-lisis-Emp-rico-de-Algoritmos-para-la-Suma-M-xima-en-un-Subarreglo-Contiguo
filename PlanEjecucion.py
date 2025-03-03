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

# Función para medir el tiempo de ejecución
def measure_time(algorithm, arr):
    start = time.time()
    result = algorithm(arr)
    end = time.time()
    return end - start, result

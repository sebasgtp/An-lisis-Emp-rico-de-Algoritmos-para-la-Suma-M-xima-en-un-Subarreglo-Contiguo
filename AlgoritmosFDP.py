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



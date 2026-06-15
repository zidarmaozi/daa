import pandas as pd
import time
import sys
import copy
import random

# Menaikkan batas rekursi agar tidak error pada data besar
sys.setrecursionlimit(5000)

#import Dataset 
df = pd.read_csv(r'C:\Users\ASUS\OneDrive\semester 4\DESAIN & ANALISIS ALGORITMA\CODING\artikel\youtube_top_1000_by_subscribers-selected-columns.csv')
data = df.to_dict('records')

# IMPLEMENTASI QUICK SORT 
def quick_sort(arr, awal, akhir, descending=False):
    if awal < akhir:
        indeks_pivot = partition(arr, awal, akhir, descending)
        quick_sort(arr, awal, indeks_pivot - 1, descending)
        quick_sort(arr, indeks_pivot + 1, akhir, descending)

def partition(arr, awal, akhir, descending):
    # Mengambil elemen pertama (low) sebagai pivot sesuai pseudocode
    nilai_pivot = arr[awal]['views'] 
    j = awal
    
    # traversal low+1..high
    for i in range(awal + 1, akhir + 1):
        # Membandingkan berdasarkan jumlah views
        condition = arr[i]['views'] >= nilai_pivot if descending else arr[i]['views'] < nilai_pivot
        
        if condition:
            j += 1
            arr[i], arr[j] = arr[j], arr[i] # swap S[i] dan S[j]
            
    # swap S[low] dan S[pivotpoint]
    arr[awal], arr[j] = arr[j], arr[awal] 
    return j


# IMPLEMENTASI MERGE SORT 
def merge_sort(arr, awal, akhir, descending=False):
    if awal < akhir:
        tengah = (awal + akhir) // 2
        merge_sort(arr, awal, tengah, descending)
        merge_sort(arr, tengah + 1, akhir, descending)
        merge(arr, awal, tengah, akhir, descending)

def merge(arr, awal, tengah, akhir, descending):
    n1 = tengah - awal + 1
    n2 = akhir - tengah
    
    L = arr[awal : tengah + 1]
    R = arr[tengah + 1 : akhir + 1]
    
    i = 0
    j = 0
    k = awal
    
    while i < n1 and j < n2:
        condition = L[i]['views'] >= R[j]['views'] if descending else L[i]['views'] <= R[j]['views']
        
        if condition:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
        
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
        
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

# IMPLEMENTASI HEAP SORT 
def siftdown(arr, n, i, descending):
    terbesar = i 
    anak_kiri = 2 * i + 1
    anak_kanan = 2 * i + 2
    
    if not descending: # Max-Heap untuk urutan Ascending
        if anak_kiri < n and arr[anak_kiri]['views'] > arr[terbesar]['views']:
            terbesar = anak_kiri
        if anak_kanan < n and arr[anak_kanan]['views'] > arr[terbesar]['views']:
            terbesar = anak_kanan
    else: # Min-Heap untuk urutan Descending
        if anak_kiri < n and arr[anak_kiri]['views'] < arr[terbesar]['views']:
            terbesar = anak_kiri
        if anak_kanan < n and arr[anak_kanan]['views'] < arr[terbesar]['views']:
            terbesar = anak_kanan
            
    if terbesar != i:
        arr[i], arr[terbesar] = arr[terbesar], arr[i]
        siftdown(arr, n, terbesar, descending)

def heap_sort(arr, descending=False):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        siftdown(arr, n, i, descending)
        
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i] # Pindah akar ke akhir
        siftdown(arr, i, 0, descending)
    return arr


# Skenario Pengujian (Benchmarking)

sizes = [100, 500, 1000]

print(f"{'N':<5} | {'Arah Urutan':<25} | {'Quick Sort':<12} | {'Merge Sort':<12} | {'Heap Sort':<12}")
print("-" * 75)

for n in sizes:
    subset_data = data[:n]
    
    random.seed(42)
    random_data = copy.deepcopy(subset_data)
    random.shuffle(random_data)
    
    scenarios = [
        ("ascending", False), 
        ("descending", True)
    ]
    
    for scenario_name, is_desc in scenarios:
        t_quick_tot = t_merge_tot = t_heap_tot = 0
        runs = 10 
        
        for _ in range(runs):
            # Pengujian Quick Sort
            arr_q = copy.deepcopy(random_data)
            t0 = time.perf_counter()
            quick_sort(arr_q, 0, len(arr_q) - 1, descending=is_desc)
            t_quick_tot += (time.perf_counter() - t0) * 1000
            
            # Pengujian Merge Sort
            arr_m = copy.deepcopy(random_data)
            t0 = time.perf_counter()
            merge_sort(arr_m, 0, len(arr_m) - 1, descending=is_desc)
            t_merge_tot += (time.perf_counter() - t0) * 1000
            
            # Pengujian Heap Sort
            arr_h = copy.deepcopy(random_data)
            t0 = time.perf_counter()
            heap_sort(arr_h, descending=is_desc)
            t_heap_tot += (time.perf_counter() - t0) * 1000
            
        print(f"{n:<5} | {scenario_name:<25} | {t_quick_tot/runs:<10.3f}ms | {t_merge_tot/runs:<10.3f}ms | {t_heap_tot/runs:<10.3f}ms")
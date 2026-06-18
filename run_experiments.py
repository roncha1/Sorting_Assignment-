import argparse
import matplotlib.pyplot as plt
import random
import statistics
import time


def insertion_sort(A):
    n = len(A)
    for i in range(1, n):
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j = j - 1
        A[j + 1] = key


def merge(A, p, q, r):
    n_L = q - p + 1
    n_R = r - q
    L = [0] * n_L
    R = [0] * n_R
    for i in range(n_L):
        L[i] = A[p + i]
    for j in range(n_R):
        R[j] = A[q + 1 + j]
    i = 0
    j = 0
    k = p
    while i < n_L and j < n_R:
        if L[i] <= R[j]:
            A[k] = L[i]
            i = i + 1
        else:
            A[k] = R[j]
            j = j + 1
        k = k + 1
    while i < n_L:
        A[k] = L[i]
        i = i + 1
        k = k + 1
    while j < n_R:
        A[k] = R[j]
        j = j + 1
        k = k + 1


def merge_sort(A, p, r):
    if p >= r:
        return
    q = (p + r) // 2
    merge_sort(A, p, q)
    merge_sort(A, q + 1, r)
    merge(A, p, q, r)


def bubble_sort(A):
    n = len(A)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                swapped = True
        if not swapped:
            break


def create_nearly_sorted_array(n, noise_percentage):
    arr = list(range(1, n + 1))
    num_swaps = int(n * (noise_percentage / 100))
    for _ in range(num_swaps):
        idx1 = random.randint(0, n - 1)
        idx2 = random.randint(0, n - 1)
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr


# =========================================================================
# PART D - COMMAND LINE INTERFACE
# =========================================================================
parser = argparse.ArgumentParser(
    description="Run customized sorting algorithm experiments."
)
parser.add_argument(
    "-a",
    nargs="+",
    type=int,
    required=True,
    help="Algorithm IDs: 1 (Bubble Sort), 3 (Insertion Sort), 4 (Merge Sort)",
)
parser.add_argument("-s", nargs="+", type=int, required=True, help="Array sizes")
parser.add_argument(
    "-e",
    type=int,
    choices=[1, 2],
    default=None,
    help="1 (5% noise), 2 (20% noise). Omit for fully random arrays.",
)
parser.add_argument(
    "-r", type=int, default=10, help="Number of repetitions per size"
)

args = parser.parse_args()

sizes = args.s
REPETITIONS = args.r
chosen_algorithms = args.a
experiment_type = args.e

# Setup dictionaries dynamically based on user selection
times_data = {algo_id: {size: [] for size in sizes} for algo_id in chosen_algorithms}

# Setup plotting title and filename dynamically based on experiment type
if experiment_type == 1:
    noise_level = 5
    plot_title = "Runtime Comparison (Nearly Sorted, Noise=5%)"
    filename = "result2.png"
elif experiment_type == 2:
    noise_level = 20
    plot_title = "Runtime Comparison (Nearly Sorted, Noise=20%)"
    filename = "result2.png"
else:
    noise_level = None
    plot_title = "Runtime Comparison (Random Arrays)"
    filename = "result1.png"

# =========================================================================
# MAIN EXPERIMENT LOOP
# =========================================================================

for n in sizes:
    for rep in range(REPETITIONS):

        # Generate data based on experiment type (-e)
        if noise_level is not None:
            base_array = create_nearly_sorted_array(n, noise_level)
        else:
            base_array = [random.randint(1, 100000) for _ in range(n)]

        # Dynamically execute only the requested algorithms (-a)
        if 1 in chosen_algorithms:
            arr_bubble = base_array.copy()
            start = time.time()
            bubble_sort(arr_bubble)
            end = time.time()
            times_data[1][n].append(end - start)

        if 3 in chosen_algorithms:
            arr_insertion = base_array.copy()
            start = time.time()
            insertion_sort(arr_insertion)
            end = time.time()
            times_data[3][n].append(end - start)

        if 4 in chosen_algorithms:
            arr_merge = base_array.copy()
            start = time.time()
            merge_sort(arr_merge, 0, len(arr_merge) - 1)
            end = time.time()
            times_data[4][n].append(end - start)

# =========================================================================
# GRAPH GENERATION
# =========================================================================
plt.figure(figsize=(10, 6))

algo_meta = {
    1: {"label": "Bubble Sort", "color": "tab:blue", "marker": "o"},
    3: {"label": "Insertion Sort", "color": "tab:orange", "marker": "s"},
    4: {"label": "Merge Sort", "color": "tab:green", "marker": "^"},
}

for algo_id in chosen_algorithms:
    if algo_id not in algo_meta:
        continue  # Ignore non-existent IDs (like 2 and 5) safely

    avg_line = []
    std_line = []

    for n in sizes:
        avg_line.append(statistics.mean(times_data[algo_id][n]))
        std_line.append(statistics.stdev(times_data[algo_id][n]))

    meta = algo_meta[algo_id]
    plt.plot(
        sizes, avg_line, label=meta["label"], marker=meta["marker"], color=meta["color"]
    )
    plt.fill_between(
        sizes,
        [avg - std for avg, std in zip(avg_line, std_line)],
        [avg + std for avg, std in zip(avg_line, std_line)],
        alpha=0.2,
        color=meta["color"],
    )

plt.title(plot_title, fontsize=14)
plt.xlabel("Array size (n)", fontsize=12)
plt.ylabel("Runtime (seconds)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(loc="upper left")

plt.savefig(filename, dpi=300)
plt.close()

print(f" Experiment completed and '{filename}' has been generated.")
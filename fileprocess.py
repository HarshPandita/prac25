from collections import defaultdict

# Sample input
files = [
    {"size": 100, "collectionIds": ["A", "B"]},
    {"size": 200, "collectionIds": ["B", "C"]},
    {"size": 300, "collectionIds": ["A"]},
    {"size": 400, "collectionIds": ["D", "A"]},
    {"size": 500, "collectionIds": ["C"]},
]

def generate_report(files, top_n=3):
    collection_sizes = defaultdict(int)
    total_size = 0

    for file in files:
        size = file["size"]
        total_size += size
        for cid in file["collectionIds"]:
            collection_sizes[cid] += size

    # Sort and get top N collections by size
    sorted_collections = sorted(collection_sizes.items(), key=lambda x: x[1], reverse=True)
    top_collections = sorted_collections[:top_n]

    return total_size, top_collections


# Example usage
total, top_collections = generate_report(files, top_n=3)
print("Total Size:", total)
print("Top Collections by Size:")
for cid, size in top_collections:
    print(f"Collection {cid}: {size}")



# -----------with lock-----------------

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import threading

# Sample input
files = [
    {"size": 100, "collectionIds": ["A", "B"]},
    {"size": 200, "collectionIds": ["B", "C"]},
    {"size": 300, "collectionIds": ["A"]},
    {"size": 400, "collectionIds": ["D", "A"]},
    {"size": 500, "collectionIds": ["C"]},
]

collection_sizes = defaultdict(int)
lock = threading.Lock()


def process_file(file):
    size = file["size"]
    for cid in file["collectionIds"]:
        with lock:
            collection_sizes[cid] += size


def generate_report(files, top_n=3, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_file, files)

    total_size = sum(file["size"] for file in files)

    # Sort dictionary by size in descending order and slice top_n
    sorted_collections = sorted(collection_sizes.items(), key=lambda x: x[1], reverse=True)
    top_collections = sorted_collections[:top_n]

    return total_size, top_collections


# Example usage
total, top_collections = generate_report(files, top_n=3)
print("Total Size:", total)
print("Top Collections by Size:")
for cid, size in top_collections:
    print(f"Collection {cid}: {size}")


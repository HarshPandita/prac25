from collections import defaultdict
import heapq
# o(nlogk)
def generate_report(files, top_n=3):
    collection_sizes = defaultdict(int)
    total_size = 0

    # Step 1: Build collection sizes and total size
    for file in files:
        size = file["size"]
        total_size += size
        for cid in file["collectionIds"]:
            collection_sizes[cid] += size

    # Step 2: Maintain a min-heap of size top_n
    min_heap = []  # (size, collectionId)
    for cid, size in collection_sizes.items():
        heapq.heappush(min_heap, (size, cid))
        if len(min_heap) > top_n:
            heapq.heappop(min_heap)

    # Step 3: Convert heap to sorted list (descending by size)
    top_collections = [(cid, size) for size, cid in sorted(min_heap, reverse=True)]

    return total_size, top_collections

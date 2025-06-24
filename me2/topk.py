from collections import Counter
import heapq
#tc: o(nlogk)
def topKFrequent(nums, k):
    # Step 1: Count frequencies
    freq_map = Counter(nums)

    # Step 2: Build min-heap of (frequency, num)
    min_heap = []

    for num, freq in freq_map.items():
        heapq.heappush(min_heap, (freq, num))
        if len(min_heap) > k:
            heapq.heappop(min_heap)  # remove least frequent

    # Step 3: Extract the numbers from the heap
    return [num for freq, num in min_heap]
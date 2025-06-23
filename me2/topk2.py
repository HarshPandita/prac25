from collections import defaultdict

# O(n)
def topKFrequent(nums, k):
    freq_map = defaultdict(int)

    # Step 1: Frequency count
    for num in nums:
        freq_map[num] += 1

    # Step 2: Bucket sort by frequency
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in freq_map.items():
        buckets[freq].append(num)

    # Step 3: Collect top k frequent elements from the end of buckets
    result = []
    for freq in range(len(buckets) - 1, 0, -1):  # from high freq to low
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result

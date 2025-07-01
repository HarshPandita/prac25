import heapq
#o(nlogkn
def assign_courts(intervals):
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0]) #o(nlog(n))

    # List of (end_time, court_id)
    court_heap = [] 
    court_assignments = {}
    court_id_counter = 1

    for interval in intervals:
        start, end = interval
        # assigned = False

        # Try to reuse a court (check earliest end time)
        if court_heap and court_heap[0][0] <= start:
            earliest_end, court_id = heapq.heappop(court_heap)
            court_assignments[court_id].append(interval)
            heapq.heappush(court_heap, (end, court_id))
            # assigned = True
        else:
            # Allocate new court
            court_id = court_id_counter
            court_id_counter += 1
            court_assignments[court_id] = [interval]
            heapq.heappush(court_heap, (end, court_id))

    return court_assignments


# # Example usage
# intervals = [[1, 4], [4, 5], [2, 4]]
# result = assign_courts(intervals)
# for court, slots in result.items():
#     print(f"Court {court}: {slots}")
# import heapq

# intervals = [[1, 4], [4, 5], [2, 4]]

# def assign_courts(intervals):
#     intervals.sort(key=lambda x:x[0])

#     court_heap = []

#     court_map = {}
#     court_id_ctr = 1

#     for interval in intervals:
#         start, end  = interval
#         # earlies ending court heaing
#         if court_heap and court_heap[0][0]<=start:
#             earliest_end, court_id = heap.heappop(court_heap)
#             court_map[court_id].append(interval)
#             heapq.heappush(heap, (end, court_id))

#         else:
#             court_id = court_id_ctr
#             court_id_ctr+=1
#             court_map[court_id] = [interval]
#             heapq.heappush(heap, (end, court_id))

#     return court_map

# intervals = [[1, 4], [4, 5], [2, 4]]
# result = assign_courts(intervals)
# for court, slots in result.items():
#     print(f"Court {court}: {slots}")
from collections import defaultdict
import heapq



class VoteSystem:
    def __init__(self):
        self.emp_map = defaultdict()
        self.heap = []

    def add_emp(self, emp_id): #O(1)
        if emp_id in self.emp_map:
            print("employee already exists")

        else:
            self.emp_map[emp_id] = 0

    def grade(self, emp_id, points): 
        self.emp_map[emp_id] += points #O(1)
        heapq.heappush(self.heap, (-self.emp_map[emp_id], emp_id)) #O(log n)

    def get_score(self,emp_id):
        print(self.emp_map[emp_id]) #O(1)

    def leaderboard(self, k):
        # return sorted(
        #     self.emp_map.items(),
        #     key=lambda x: x[1],
        #     reverse=True
        # )
        result = []
        temp = []
        while self.heap and len(result)<k: #o(k)
            value = heapq.heappop(self.heap) #o(log n)

            if -value[0] == self.emp_map[value[1]]:
                result.append((value[1],-value[0])) #O(1)
                temp.append((value[0], value[1])) #O(1)

        for entry in temp: #O(k)
            heapq.heappush(self.heap,(entry[0],entry[1])) #O(log n)
        return result


vs= VoteSystem()
vs.add_emp("emp1")
vs.add_emp("emp2")
vs.add_emp("emp3")

vs.grade("emp1", 10)
vs.grade("emp2", 20)
vs.grade("emp3", 15)

print(vs.emp_map)
print(vs.heap)
print(vs.leaderboard(2))
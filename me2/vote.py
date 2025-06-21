class Candidate:
    def __init__(self, name, score, timestamp):
        self.name = name
        self.score = score
        self.timestamp = timestamp
    def __lt__(self, other):
        # Sort by score DESC
        if self.score != other.score:
            return self.score > other.score
        # If score is same, earlier timestamp wins
        return self.timestamp < other.timestamp
    
def getResults(votes):
    timestamps = {}
    points = {}
    globalts = 0

    for ballots in votes:
        for idx, candidate in enumerate(ballots):
            curr_point = 3-idx
            if candidate not in points:
                points[candidate] = 0

            points[candidate] += curr_point
            globalts+=1
            timestamps[candidate] = globalts



    candidates = []

    for name in points:
        candidates.append(Candidate(name, points[name], timestamps[name]))
    
    candidates.sort()
    return [c.name for c in candidates]


ballots = [
    ["Alice", "Bob", "Charlie"],
    ["Bob", "Alice", "Charlie"],
    ["Charlie", "Alice", "Bob"]
]

# Scoring:
# Alice: 3 (1st) + 2 (2nd) + 2 (2nd) = 7
# Bob:   2 (2nd) + 3 (1st) + 1 (3rd) = 6
# Charlie: 1 (3rd) + 1 (3rd) + 3 (1st) = 5

print(getResults(ballots))  
# Output: ['Alice', 'Bob', 'Charlie']
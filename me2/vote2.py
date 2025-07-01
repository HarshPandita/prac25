
# O(n+clogc)

def getResults(ballots):
    from collections import defaultdict

    scores = defaultdict(int)           # candidate -> total points
    reached_at = {}                     # candidate -> time when final score was reached

    for timestamp, ballot in enumerate(ballots):
        for rank, candidate in enumerate(ballot):
            points = 3 - rank           # 1st place = 3, 2nd = 2, 3rd = 1
            scores[candidate] += points
            # Update time only if this point changes their score
            reached_at[candidate] = timestamp  # Last time their score changed

    # Convert to a sortable list
    result = []
    for candidate, total in scores.items():
        result.append((candidate, total, reached_at[candidate]))

    # Sort by:
    # - Total score descending
    # - Timestamp ascending
    result.sort(key=lambda x: (-x[1], x[2]))

    return [name for name, _, _ in result]

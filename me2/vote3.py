from collections import defaultdict
# o(n*m) + o(c.logc)
def rankCandidates(votes):
    score = defaultdict(int)
    reached_at = {}  # candidate -> timestamp when final score was reached

    for t, ballot in enumerate(votes):
        for i, candidate in enumerate(ballot):
            points = len(ballot) - i
            score[candidate] += points
            reached_at[candidate] = t  # always update to current time

    # But now go back and re-compute when they reached their final score
    # so that we get the first time they *reached their final score*
    final_score = dict(score)
    score = defaultdict(int)
    reached_at = {}

    for t, ballot in enumerate(votes):
        for i, candidate in enumerate(ballot):
            points = len(ballot) - i
            score[candidate] += points
            if score[candidate] == final_score[candidate] and candidate not in reached_at:
                reached_at[candidate] = t

    # Sort by:
    # - total score descending
    # - earliest timestamp when final score was reached
    result = sorted(final_score.items(), key=lambda x: (-x[1], reached_at[x[0]]))

    return [name for name, _ in result]

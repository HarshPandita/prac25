from collections import deque


class Article:
    def __init__(self, article_id, name):
        self.article_id = article_id
        self.name = name
        self.upvotes = 0
        self.downvotes = 0

    def score(self):
        return self.upvotes - self.downvotes


class VotingSystem:
    def __init__(self):
        self.next_article_id = 1
        self.articles = {}
        self.user_votes = {}
        self.flip_history = {}
        self.last_voted_article = {}

    def addArticle(self, name):
        article = Article(self.next_article_id, name)
        self.articles[self.next_article_id] = article
        self.next_article_id += 1

    def _vote(self, userId, articleId, new_vote):

        if userId not in self.user_votes:
            self.user_votes[userId] = {} # O(1)

        if userId not in self.flip_history:
            self.flip_history[userId] = deque() #O(1)

        article = self.articles[articleId] #O(1)
        prev_vote = self.user_votes[userId].get(articleId)  #O(1)

        # Detect vote flip
        if prev_vote is not None and prev_vote != new_vote:
            flips = self.flip_history[userId]

            if articleId in flips: #O(3)
                flips.remove(articleId) #O(3)

            flips.appendleft(articleId) #O(1)

            # Keep only last 3
            if len(flips) > 3:
                flips.pop() #O(1)

        # Adjust vote counts
        if prev_vote == 1:
            article.upvotes -= 1
        elif prev_vote == -1:
            article.downvotes -= 1

        if new_vote == 1:
            article.upvotes += 1
        else:
            article.downvotes += 1

        self.user_votes[userId][articleId] = new_vote
        self.last_voted_article[userId] = articleId

    def upvote(self, userId, articleId):
        self._vote(userId, articleId, 1)

    def downvote(self, userId, articleId):
        self._vote(userId, articleId, -1)

    def last3Flips(self, userId):
        if userId not in self.flip_history:
            return []
        return list(self.flip_history[userId])

    def lastVotedArticle(self, userId):
        return self.last_voted_article.get(userId)

    def topArticlesByScore(self):
        articles_list = list(self.articles.values())
        articles_list.sort(key=lambda a: a.score(), reverse=True)
        return articles_list



vs = VotingSystem()

# -------------------------
# Add articles
# -------------------------
vs.addArticle("A1")
vs.addArticle("A2")
vs.addArticle("A3")
vs.addArticle("A4")

# -------------------------
# Basic voting
# -------------------------
vs.upvote("u1", 1)
assert vs.articles[1].upvotes == 1
assert vs.lastVotedArticle("u1") == 1

# -------------------------
# Vote flip detection
# -------------------------
vs.downvote("u1", 1)
assert vs.last3Flips("u1") == [1]

# flipping again should keep unique
vs.upvote("u1", 1)
assert vs.last3Flips("u1") == [1]

# -------------------------
# Multiple flips different articles
# -------------------------
vs.upvote("u1", 2)
vs.downvote("u1", 2)

vs.upvote("u1", 3)
vs.downvote("u1", 3)

# last 3 unique flips, most recent first
assert vs.last3Flips("u1") == [3, 2, 1]

# -------------------------
# Exceed 3 flips
# -------------------------
vs.upvote("u1", 4)
vs.downvote("u1", 4)

assert vs.last3Flips("u1") == [4, 3, 2]

# -------------------------
# Same vote again → no flip
# -------------------------
vs.upvote("u2", 1)
vs.upvote("u2", 1)
assert vs.last3Flips("u2") == []

# -------------------------
# Article score sorting
# -------------------------
sorted_articles = vs.topArticlesByScore()
scores = [a.score() for a in sorted_articles]
assert scores == sorted(scores, reverse=True)

# -------------------------
# Last voted article tracking
# -------------------------
vs.downvote("u2", 2)
assert vs.lastVotedArticle("u2") == 2

print("All tests passed ✅")
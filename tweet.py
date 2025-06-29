import heapq
from collections import defaultdict

class Tweeter:
    def __init__(self):
        self.timestamp = 0
        self.userTweets = defaultdict(list)  # userId → list of (timestamp, tweetId)
        self.userFollowers = defaultdict(set)

    def postTweet(self, userId, tweetId, tweetDesc=None):
        self.userTweets[userId].append((self.timestamp, tweetId))
        self.timestamp += 1

    def follow(self, userId, followeeId):
        self.userFollowers[userId].add(followeeId)

    def unfollow(self, userId, followeeId):
        self.userFollowers[userId].discard(followeeId)

    def getNewsFeed(self, userId):
        self.userFollowers[userId].add(userId)  # Ensure self-follow

        maxHeap = []
        # O(no. of followers)
        for followeeId in self.userFollowers[userId]:
            tweets = self.userTweets.get(followeeId, [])
            if tweets:
                index = len(tweets) - 1  # Start from latest tweet
                timestamp, tweetId = tweets[index]
                # Push: (-timestamp, tweetId, followeeId, index)
                heapq.heappush(maxHeap, (-timestamp, tweetId, followeeId, index))

        result = []
        # o(10logf)
        while maxHeap and len(result) < 10:
            negTs, tweetId, uid, idx = heapq.heappop(maxHeap)
            result.append(tweetId)
            if idx > 0:
                # Push the next most recent tweet of this user
                nextTs, nextTweetId = self.userTweets[uid][idx - 1]
                heapq.heappush(maxHeap, (-nextTs, nextTweetId, uid, idx - 1))

        return result

    # def getNewsFeed(self, userId):
    #     if userId not in self.userFollowers:
    #         self.userFollowers[userId]=set()
    #     self.userFollowers[userId].add(userId)

    #     allFollowers = self.userFollowers[userId]
    #     heap = []
    #     for follower in allFollowers:
            
    #         posts = self.userTweets[follower]
    #         for post in posts[-10:]:
    #             heapq.heappush(heap, (post[0],post[1]))
    #             if len(heap)>10:
    #                 heapq.heappop(heap)
            
    #     return [tweetId for _, tweetId in sorted(heap, reverse=True)]

# twitter = Tweeter()
# twitter.postTweet(1, 5)
# print(twitter.getNewsFeed(1))  # ➞ [5]

# twitter.postTweet(2, 6)
# twitter.follow(1, 2)
# print(twitter.getNewsFeed(1))  # ➞ [6, 5] (6 is newer than 5)


# twitter.unfollow(1, 2)
# print(twitter.getNewsFeed(1))  # ➞ [5] (user 1 no longer sees user 2's tweet)

# for i in range(10):
#     twitter.postTweet(1, 100 + i)
# print(twitter.getNewsFeed(1))  # ➞ [109, 108, ..., 100]



twitter = Tweeter()
twitter.postTweet(1, 10)
twitter.postTweet(3, 30)
twitter.postTweet(2, 20)
twitter.postTweet(2, 21)
twitter.follow(1, 2)
twitter.follow(1, 3)
print(twitter.getNewsFeed(1))  # ➞ [30, 21, 20, 10]




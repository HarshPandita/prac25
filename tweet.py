# ---- users # ---- user tweets
# ---- follower and following
# ---- recent tweets  -- timestamp
import heapq
class Tweeter:
    def __init__(self):
        self.timestamp = 0
        self.userTweets = {}
        self.userFollowers = {}

    
    def postTweet(self, userId, tweetId, tweetDesc = None):
        
        if userId not in self.userTweets:
            self.userTweets[userId] = []
        self.userTweets[userId].append((self.timestamp, tweetId))
        
        self.timestamp += 1

    def follow(self, userId, followeeId):
        if userId not in self.userFollowers:
            self.userFollowers[userId] = set()
        self.userFollowers[userId].add(followeeId)

    def unfollow(self, userId, followeeId):
        if userId not in self.userFollowers:
            print("No such user")
        self.userFollowers[userId].remove(followeeId)

    
    def getNewsFeed(self, userId):
        if userId not in self.userFollowers:
            self.userFollowers[userId]=set()
        self.userFollowers[userId].add(userId)

        allFollowers = self.userFollowers[userId]
        heap = []
        for follower in allFollowers:
            
            posts = self.userTweets[follower]
            for post in posts[-10:]:
                heapq.heappush(heap, (post[0],post[1]))
                if len(heap)>10:
                    heapq.heapop(heap)
            
        return [tweetId for _, tweetId in sorted(heap, reverse=True)]



twitter = Tweeter()
twitter.postTweet(1, 5)
print(twitter.getNewsFeed(1))  # ➞ [5]

twitter.postTweet(2, 6)
twitter.follow(1, 2)
print(twitter.getNewsFeed(1))  # ➞ [6, 5] (6 is newer than 5)


twitter.unfollow(1, 2)
print(twitter.getNewsFeed(1))  # ➞ [5] (user 1 no longer sees user 2's tweet)

for i in range(10):
    twitter.postTweet(1, 100 + i)
print(twitter.getNewsFeed(1))  # ➞ [109, 108, ..., 100]



twitter = Tweeter()
twitter.postTweet(1, 10)
twitter.postTweet(2, 20)
twitter.postTweet(3, 30)
twitter.postTweet(2, 21)
twitter.follow(1, 2)
twitter.follow(1, 3)
print(twitter.getNewsFeed(1))  # ➞ [30, 21, 20, 10]




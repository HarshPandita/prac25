from collections import defaultdict, deque
class MusicPlayer:
    def __init__(self):
        self.songIdCounter = 1
        self.songIdToTitle = {}                         # songId → title
        self.songIdToUserSet = defaultdict(set)         # songId → set(userIds)
        self.userToRecentSongs = defaultdict(deque)     # userId → deque of recent songIds
        # self.userToRecentSongs = defaultdict(OrderedDict) #ordered dict 
        self.userToStarredSongs = defaultdict(set)      # userId → set of starred songIds

    def addSong(self, songTitle): #O(1)
        songId = self.songIdCounter
        self.songIdCounter += 1
        self.songIdToTitle[songId] = songTitle
        return songId

    def playSong(self, songId, userId):
        if songId not in self.songIdToTitle:
            print(f"Song ID {songId} not found.")
            return

        # Track unique users for this song
        self.songIdToUserSet[songId].add(userId)

        # Update user's recent song history
        recent = self.userToRecentSongs[userId]
        if songId in recent:
            recent.remove(songId) #O(N) - deque removal
        recent.appendleft(songId)
        if len(recent) > 3:
            recent.pop()

    # def playSong(self, songId, userId):
    #     recent = self.userToRecentSongs[userId]
    #     if songId in recent:
    #         del recent[songId]
    #     recent[songId] = None
    #     if len(recent) > 3:
    #         recent.popitem(last=False)

    def starSong(self, songId, userId): #O(1)
        if songId not in self.songIdToTitle:
            print(f"Song ID {songId} not found.")
            return
        self.userToStarredSongs[userId].add(songId)

    def unstarSong(self, songId, userId): #O(1)
        self.userToStarredSongs[userId].discard(songId)

    def isStarred(self, songId, userId): #O(1)
        return songId in self.userToStarredSongs[userId]

    def getStarredSongs(self, userId):
        return [self.songIdToTitle[songId] for songId in self.userToStarredSongs[userId]]

    def printMostPlayedSongs(self): #o(Nlogk)
        # Build a list of (songId, uniqueUserCount)
        songList = [(songId, len(users)) for songId, users in self.songIdToUserSet.items()]
        songList.sort(key=lambda x: (-x[1], self.songIdToTitle[x[0]]))  # Sort by count desc, then title

        for songId, count in songList:
            print(f"{self.songIdToTitle[songId]} ({count} unique plays)")

    def getLastThreeSongs(self, userId): #(O(1))
        return list(self.userToRecentSongs[userId])
    
    #  only if needed
    # import heapq

    # def printTopKMostPlayedSongs(self, k=5):
    #     heap = []

    #     for songId, users in self.songIdToUserSet.items():
    #         count = len(users)
    #         title = self.songIdToTitle[songId]
    #         heapq.heappush(heap, (count, title, songId))
    #         if len(heap) > k:
    #             heapq.heappop(heap)  # Keep only top K

    #     # Largest first
    #     for count, title, songId in sorted(heap, reverse=True):
    #         print(f"{title} ({count} unique plays)")

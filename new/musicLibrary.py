from collections import defaultdict, OrderedDict
import heapq
class MusicLibrary:
    def __init__(self):
        self.songIdToTitle = defaultdict()
        self.id = 1
        self.songToUserMap = defaultdict(set)
        self.userToRecentMap = defaultdict(OrderedDict)


    def addSong(self, title):
        self.songIdToTitle[self.id] = title
        self.id+=1

    def playSong(self, songId, userId):
        self.songToUserMap[songId].add(userId)
        if songId in self.userToRecentMap[userId]:
            del self.userToRecentMap[userId][songId]
        self.userToRecentMap[userId][songId] = None
        if len(self.userToRecentMap[userId]) > 3:
            self.userToRecentMap[userId].popitem(last=False)

    def getRecentSongs(self, userId):
        self.userToRecentMap[userId]
        print(f"Recent songs for user {userId}")
        for songId in reversed(list(self.userToRecentMap[userId].keys())):
            print(f"{self.songIdToTitle[songId]}")

    def getTopKPlayedSongs(self, k):
        heap = []
        for songId, plays in self.songToUserMap.items():
            count = len(plays)
            heapq.heappush(heap, (count, songId))
            if len(heap) > k:
                heapq.heappop(heap)


        for detail in reversed(heap):
            print(f"Song ID {detail[1]} was played {detail[0]} times")



library = MusicLibrary()
library.addSong("Shape of You")
library.addSong("B")
library.playSong(1, "user1")
library.playSong(1, "user2")
library.playSong(2, "user2")
library.playSong(2, "user2")
print(library.songIdToTitle)
(library.getRecentSongs("user1"))
library.getTopKPlayedSongs(2)
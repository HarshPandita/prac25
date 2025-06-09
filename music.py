# design music library:
#     play song
#     get top k songs


# song map (track songs and how many times were they played)
# user to song map (which user played what song) value should be a deque if we want to track latest 

from collections import deque
import heapq
class MusicLib:
    def __init__(self):
        self.songPlayedCount = {}
        self.userSongMap = {}  
    def playSong(self, user, song):
        if song not in self.songPlayedCount:
            self.songPlayedCount[song]=1

        self.songPlayedCount[song]+=1
        
        if user not in self.userSongMap:
            self.userSongMap[user]=deque()

        print(f"adding song {song} to user {user} map")
        self.userSongMap[user].append(song)
        print(f"user map {self.userSongMap[user]}")

        if len(self.userSongMap[user]) > 3:
            self.userSongMap[user].popleft()
    def getTopKSongs(self, k):
        heapForTrack = []
        for item, val in self.songPlayedCount.items():
            heapq.heappush(heapForTrack,(-val, item))

        result = []

        for item in range(min(len(heapForTrack), k)):
            result.append(heapq.heappop(heapForTrack)[1])
        return result
    def geRecentSongs(self, user):
    
        return self.userSongMap[user]


lib = MusicLib()
lib.playSong("Alice", "SongA")
lib.playSong("Bob", "SongA")
lib.playSong("Alice", "SongB")
lib.playSong("Alice", "SongC")
lib.playSong("Alice", "SongA")  # Played again by same user

print(lib.getTopKSongs(2))           # ['SongA', 'SongB']
print(lib.geRecentSongs("Alice"))
            
        


        


        


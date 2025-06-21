from collections import defaultdict, deque

class MusicPlayer:
    def __init__(self):
        self.songIdCounter = 1
        self.songIdToTitle = {}                         # songId → title
        self.songIdToUserSet = defaultdict(set)         # songId → set(userIds)
        self.userToRecentSongs = defaultdict(deque)     # userId → deque (unique recent songs)

    def addSong(self, songTitle):
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
            recent.remove(songId)
        recent.appendleft(songId)
        if len(recent) > 3:
            recent.pop()

    def printMostPlayedSongs(self):
        # Build a list of (songId, uniqueUserCount)
        songList = [(songId, len(users)) for songId, users in self.songIdToUserSet.items()]
        songList.sort(key=lambda x: (-x[1], self.songIdToTitle[x[0]]))  # Sort by user count desc, then title
        
        for songId, count in songList:
            print(f"{self.songIdToTitle[songId]} ({count} unique plays)")

    def getLastThreeSongs(self, userId):
        return list(self.userToRecentSongs[userId])

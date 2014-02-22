"""
Created on 21.02.2014

@author: Carbon
"""
CLIENT_SPECTATOR = 2
CLIENT_PLAYER_WHITE = 0
CLIENT_PLAYER_BLACK = 1

class Client:
    """
    classdocs
    """
    def __init__(self, connection):
        '''
        Constructor
        '''
        self._connection = connection
        self.gameId = -1
        self.mode = -1
    
    def joinedGame(self, game):
        self.gameId
    
    def readLine(self):
        return 'PLACEHOLDER'
    
    def sendMove(self, move):
        self._connection
        
    def sendCode(self, code):
        pass
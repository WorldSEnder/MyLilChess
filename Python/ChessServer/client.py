"""Created on 21.02.2014

@author: WorldSEnder"""
from random import Random
from responseCodes import CHAT_MESSAGE_SERVER_SHUTDOWN
__author__ = 'WorldSEnder'
__version__ = 0.1

CLIENT_UNDECIDED = -1
CLIENT_PLAYER_WHITE = 0
CLIENT_PLAYER_BLACK = 1
CLIENT_SPECTATOR = 2
CLIENT_HTTP = 100
CLIENT_ADMIN = 999

class Client:
    """Represents a connected client."""
    def __init__(self, connection):
        """Constructor"""
        self._connection = connection
        self.gameId = -1
        self.mode = CLIENT_UNDECIDED
        self.name = 'client' + Random().randint(0, 999)
    
    def readLine(self, block):
        return self._connection.getLine(block)
    
    def sendMove(self, move):
        self._connection
        return
    
    def sendCode(self, code, *args):
        def toArgsIter(*args):
            for a in args:
                yield str(a)
        if code < 0:
            return
        self._connection.sendAll(' '.join(toArgsIter(code, *args)))
        return
    
    def getName(self):
        return self.name
    
    def closeConnectionGracefully(self):
        self._connection.sendCode(CHAT_MESSAGE_SERVER_SHUTDOWN)
        return

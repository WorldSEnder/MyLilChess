"""Created on 21.02.2014

@author: WorldSEnder"""
from responseCodes import GAME_JOINED_SPECTATOR, GAME_JOINED_UNSUCCESFUL, \
    GAME_STATE_SPECTATOR_JOIN
__author__ = "WorldSEnder"
__version__ = 0.2

from threading import Thread
from utils import static_var
MOVE_PLAYER_WHITE = 0
MOVE_PLAYER_BLACK = 1

cleanBoard = (".........." +
              ".........." +
              ".RKB+QBKR." +
              ".PPPPPPPP." +
              ".........." +
              ".........." +
              ".........." +
              ".........." +
              ".pppppppp." +
              ".rkb+qbkr." +
              ".........." +
              ".........." )

class Game(Thread):
    """Represents a game, is a self-running thread"""
    
    @static_var('nextId', 0)
    @staticmethod
    def requestNextGameId():
        retid = Game.requestNextGameId.nextId
        Game.requestNextGameId.nextId += 1
        return retid
    
    def __init__(self, playerWhite, playerBlack):
        """Constructor"""
        # contains the two players and the spectators
        self._players = [playerWhite, playerBlack]
        self.inProgress = True
        self.movingPlayer = MOVE_PLAYER_WHITE
        self.history = History()
        self.gameId = Game.requestNextGameId()
        self.board = cleanBoard
    
    def run(self):
        while self.inProgress:
            for client in self._players[:]:
                line = client.readLine()
                self.handleLine(line, client)
            del client
        return
    
    def handleLine(self, line, client):
        """Handles a single line coming from the client"""
        if not self.inProgress:
            return
        raise NotImplementedError()
    
    def spectatorJoin(self, spectator):
        """Joins a spectator into the game."""
        if not self.inProgress:
            spectator.sendCode(GAME_JOINED_UNSUCCESFUL)
            return False
        nameList = []
        for client in self._players:
            client.sendCode(GAME_STATE_SPECTATOR_JOIN, spectator.getName())
            nameList.append(client.getName())
        self._players.append(spectator)
        del client
        spectator.sendCode(GAME_JOINED_SPECTATOR, *nameList)
        return
    
    def _move(self, playerMoving, move):
        """emulates the current move on the board.
        Returns a result as a response-code - look at .responseCodes"""
        raise NotImplementedError()
    
    def interrupt(self):
        """Interrupts the game, sending a terminate signal to all 
        clients"""
        raise NotImplementedError()

Game.requestNextGameId.nextId = 0

class History:
    """Represents a game-history"""
    def __init__(self):
        self._backingArray = []
    
    def _pairs(self):
        i = iter(self._backingArray)
        for a in i:
            yield (a, next(i, ''))
        del a
        return
    
    def _enum(self):
        i = iter(self._backingArray)
        for idx, a in enumerate(i):
            yield (idx, (a, next(i, '')))
        del idx, a
        return
    
    def append(self, item):
        self._backingArray.append(item)
        return
    
    def clear(self):
        self._backingArray.clear()
        return
    
    def copy(self):
        h = History()
        h._backingArray = self._backingArray.copy()
        return h
    
    def count(self, value):
        return self._backingArray.count(value)
    
    def extend(self, iterable):
        self._backingArray.extend(iterable)
        return
    
    def index(self, value, start=None, stop=None):
        return self._backingArray.index(value, start, stop)
    
    def insert(self, index, obj):
        self._backingArray.insert(index, obj)
        return
    
    def pop(self, index=-1):
        self._backingArray.pop(index)
        return
    
    def remove(self, value):
        self._backingArray.remove(value)
        return
    
    def sort(self, key=None, reverse=False):
        self._backingArray.sort(key, reverse)
        return
    
    def __add__(self, y):
        self._backingArray.__add__(y)
        return self
    
    def __contains__(self, y):
        if isinstance(y, tuple):
            return y in self._pairs()
        return self._backingArray.__contains__(y)
    
    def __eq__(self, other):
        if isinstance(other, History):
            return self._backingArray == other._backingArray
        return self._backingArray == other
    
    def __iadd__(self, other):
        self._backingArray += other
        return self
    
    def __imul__(self, other):
        self._backingArray *= other
        return self
    
    def __iter__(self):
        return iter(self._enum())
    
    def __len__(self):
        return len(self._backingArray)
    
    def __mul__(self, other):
        h = History()
        h._backingArray = self._backingArray * other
        return h
    
    def __rmul__(self, other):
        h = History()
        h._backingArray = other * self._backingArray
        return h
    
    def __str__(self):
        rstr = ''
        for move, w, b in self._pairs():
            rstr += ('%s. %s %s ' % (move, w, b))
        return rstr

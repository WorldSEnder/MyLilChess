"""
Created on 21.02.2014

@author: Carbon
"""
from threading import Thread
from funcutils import static_var
from responseCodes import MOVE_RESULT_SUCCESS, MOVE_RESULT_ERROR
MOVE_PLAYER_WHITE = 0
MOVE_PLAYER_BLACK = 1

class Game(Thread):
    @static_var('nextId', 0)
    @staticmethod
    def requestNextGameId():
        retid = requestNextGameId.nextId
        requestNextGameId.nextId += 1
        return retid
    """
    classdocs
    """    
    def __init__(self, playerWhite, playerBlack):
        '''
        Constructor
        '''
        # contains the two players and the spectators
        self._players = [playerWhite, playerBlack]
        self.inProgress = True
        self.movingPlayer = MOVE_PLAYER_WHITE
        self.history = History()
        self.gameId = Game.requestNextGameId()
        
    def run(self):
        while self.inProgress:
            pass
        
    def clientJoin(self, player):
        player.gameId = self.gameId
        player.mode = min(len(self._players), 2)
        
    def handleMoveRequest(self, playerMoving, move):
        if (playerMoving ^ self.movingPlayer):
            return
        # valid player
        moveResult = self._move(playerMoving, move)
        self.afterMove(playerMoving, move, moveResult)
        
    def _move(self, playerMoving, move, revert=False):
        '''
        emulates the current move on the board.
        Returns an respondcode - 200 success
        '''
        if revert:
            raise NotImplementedError()
        
        if not self.inProgress:
            return 404
        return 200
    
    def afterMove(self, movingPlayer, move, moveResult):
        '''
        Notifies all players about the 
        '''
        # send the result to the player who sent it
        self._players[movingPlayer].sendResult(moveResult)
        # if it was a success 
        if (moveResult >= MOVE_RESULT_SUCCESS) and (moveResult < MOVE_RESULT_ERROR):
            # switch to the other player, it's his turn
            self.movingPlayer = not movingPlayer
            # append the move to the history
            self.history.append(move)
            # then send the move aswell
            for playerSpec in self._players:
                playerSpec.sendMove(move)
                
class History:
    '''
    Represents a game-history
    '''
    def __init__(self):
        self._backingArray = []
        
    def _pairs(self):
        i = iter(self._backingArray)
        for a in i:
            yield (a, next(i, ''))
            
    def _enum(self):
        i = iter(self._backingArray)
        for idx, a in enumerate(i):
            yield (idx, (a, next(i, '')))
        
    def append(self, item):
        self._backingArray.append(item)
        
    def clear(self):
        self._backingArray.clear()
        
    def copy(self):
        h = History()
        h._backingArray = self._backingArray.copy()
        return h
    
    def count(self, value):
        return self._backingArray.count(value)
    
    def extend(self, iterable):
        self._backingArray.extend(iterable)
        
    def index(self, value, start=None, stop=None):
        return self._backingArray.index(value, start, stop)
        
    def insert(self, index, obj):
        self._backingArray.insert(index, obj)
        
    def pop(self, index=-1):
        self._backingArray.pop(index)
        
    def remove(self, value):
        self._backingArray.remove(value)
        
    def sort(self, key=None, reverse=False):
        self._backingArray.sort(key, reverse)
        
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
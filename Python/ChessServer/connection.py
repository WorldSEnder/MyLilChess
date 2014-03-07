"""
Created on 21.02.2014

@author: WorldSEnder
"""
__author__ = "WorldSEnder"
__version__ = 0.1

class Connection():
    """
    classdocs
    """
    def __init__(self, clientInfo, buffSize=-1):
        """
        Constructor
        """
        self.socket = clientInfo[0]
        self._fileobject = self.socket.makefile('r', buffSize)
        self.address = clientInfo[1]
    
    def sendAll(self, message):
        self.socket.sendall(message)
        return
    
    def getLine(self, block):
        bline = self._fileobject.readline()
        if block:
            # while bline in [None, '']:
            #     bline = self._fileobject.readline()
            raise NotImplementedError()
        return bline

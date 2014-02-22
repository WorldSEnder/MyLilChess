"""
Created on 21.02.2014

@author: Carbon
"""

class Connection():
    """
    classdocs
    """
    def __init__(self, clientInfo):
        '''
        Constructor
        '''
        self.socket = clientInfo[0]
        self.address = clientInfo[1]
        
    def sendAll(self, message):
        self.socket.sendall(message)
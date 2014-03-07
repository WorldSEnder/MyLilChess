import socket
from client import Client
from connection import Connection
"""
Created on 21.02.2014

@author: WorldSEnder
"""
from lobby import Lobby
__author__ = "WorldSEnder"
__version__ = 0.1

class Server:
    def __init__(self, HOST='', PORT=33221):
        if HOST is None:
            raise ValueError('HOST cannot be None')
        self.running = False
        self.serverSock = None
        self.HOST = HOST
        self.PORT = PORT
        self.BUFFSIZE = 1024
        self.gamesThread = []
        self.lobby = Lobby(self.gamesThread)
        return
    
    def _clientConnected(self, clientInfo):
        if not self.running:
            return
        print('client connected from {}.'.format(clientInfo[1]))
        client = Client(Connection(clientInfo))
        self.lobby.listeningClients.append(client)
        return
    
    def start(self):
        self.running = True
        self.serverSock = socket.socket()
        self.serverSock.bind((self.HOST, self.PORT))
        self.HOST, self.PORT = self.serverSock.getsockname()
        self.serverSock.listen(5)
        print('Awaiting connections. . .')
        while self.running:
            newClient = self.serverSock.accept()
            self._clientConnected(newClient)
        return
    
    def stopGracefully(self):
        self.running = False
        for game in self.gamesThreads:
            game.interrupt()
        del game
        self.lobby.close()
        self.serverSock.close()
        print('Shutting down the server.')
        return

if __name__ == '__main__':
    Server().start()
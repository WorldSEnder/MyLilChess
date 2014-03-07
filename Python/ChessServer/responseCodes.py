"""
Created on 22.02.2014
This file contains response codes for the appropriate command or as a stream 
that describes changed game states, etc. 
Commands are line based messages that a client sends to the server. Each command 
might trigger (asynchronous) responds. A response code is an integer 
(inclusively) between 0 and 255 or 0x0 and 0xFF. 
The eight most significant bits contain an identifier to which command this 
is a response to. This may be evaluated by an Xor-check with the appropriate
mask (first value of each sector).
The eight least significant bits contain an identifier that closer describes
the response. This may be a sign for a successful or unsuccessful command and
is more closely described in the appropriate section below.

@author: WorldSEnder
"""
__author__ = 'WorldSEnder'
__version__ = 0.2

# STREAM server messages (for example MOTD etc.)
SERVER_MESSAGE = 0x00 # MASK

# RESPOND the sent MOVE was successful
MOVE_RESULT = 0x10 # MASK
# the MOVE was successful
MOVE_RESULT_SUCCESS = 0x10 # MASK
# the move captured an enemy 
MOVE_RESULT_CAPTURE = 0x11
# the move resulted in a check
MOVE_RESULT_CHECK = 0x12
# the move resulted in both
MOVE_RESULT_TAKE_CHECK = 0x13
# RESPOND there was an error with the MOVE given
MOVE_RESULT_ERROR = 0x18 # MASK
# the move's syntax was incorrect
#  - should send back a description of the problem
MOVE_RESULT_SYNTAX_ERROR = 0x19
# the move would cause the piece to go out-of-bounds
MOVE_RESULT_OUT_OF_BOUNDS = 0x1A
# there is no appropriate piece that can perform such a move
MOVE_RESULT_NO_PIECE = 0x1B
# the move specified is ambiguous
MOVE_RESULT_AMBIGUOUS = 0x1C
# move result not your turn
MOVE_RESULT_NOT_YOUR_TURN = 0x1D

# ASYNCH RESPOND to QUEUEJOIN, CHALLENGE 
# and SPECTATE
GAME_JOINED = 0x20
# you joined the game as the white player
#  - sends you the name of your opponent
GAME_JOINED_WHITE = 0x21
# you're the black player
#  - sends you the name of your opponent
GAME_JOINED_BLACK = 0x22
# you're a spectator
#  - should send the name of the players and spectators in-game
#  - the first two names are the names of the players. The rest
#     are spectators
GAME_JOINED_SPECTATOR = 0x23
# unsuccessfully tried to join a game
#  - maybe the Queue is full
#  - the other player declined your challenge
#  - the game doesn't allow spectators
#  - the game got shutdown while you tried to join
GAME_JOINED_UNSUCCESFUL = 0x24

# STREAM the state of the game changed
GAME_STATE_CHANGE = 0x30
# a new spectator has joined the game
#  - should send the name
GAME_STATE_SPECTATOR_JOIN = 0x31
# someone (possibly you) has left the game
#  - should send the name
#  - if it's you then this is an asynch respond to
#     a RESIGN issued by you 
#  - the one didn't get kicked
#  - the game's result is returned with a different code
GAME_STATE_PLAYER_PART = 0x32
# someone got kicked (possibly you)
#  - should send the name of the kicked person
GAME_STATE_PLAYER_KICKED = 0x33
# a move has been made on the board
# you also get this message if you made the move so
# be careful with handling this
#  - should contain the move made
GAME_STATE_MOVE_MADE = 0x34
# it's the other player's turn now
#  - includes one of (WHITE, BLACK) in case you don't know anymore
GAME_STATE_TURN = 0x35
# your opponent has offered you to agree on a tie
GAME_STATE_TIE_OFFERED = 0x36
# your opponent has declined to agree on a tie
GAME_STATE_TIE_DECLINED = 0x37
# the game ended
GAME_STATE_END = 0x38 # MASK
# the game is finished with white winning
#  - the reason for winning should be in the message:
#      DC - the enemy disconnected
#      TIMEOUT - the enemy timed out
#      FORFEIT - the enemy forfeited
#      CHECKMATE - the enemy's king has been slain
GAME_STATE_WIN_WHITE = 0x39
# the game is finished with black winning
#  - the reason for winning should be in the message:
#      DC - the enemy disconnected
#      TIMEOUT - the enemy timed out
#      FORFEIT - the enemy forfeited
#      CHECKMATE - the enemy's king has been slain
GAME_STATE_WIN_BLACK = 0x3A
# the game has been finished, no winner
#  - the reason for tie should be in the message:
#      AGREEMENT - both player agreed to end the game
#      STALEMATE - the game ended in a stalemate
GAME_STATE_TIE = 0x3B
# the game was forced to end by a server shutdown
GAME_STATE_SERVER_SHUTDOWN = 0x3C

# RESPOND chat response
CHAT_SERVER_RESPONSE = 0x40 # MASK
# nick changed
#  - will have your new nick
CHAT_NICK_CHANGED = 0x41
# you sent a message
CHAT_MESSAGE_SUCCESSFUL = 0x42
# you are not allowed to send messages
CHAT_MESSAGE_UNSUCCESSFUL_BANNED = 0x43

# STREAM messages from others
CHAT_SERVER_STREAM = 0x50 # MASK
# when another person types something into chat for you
#  - contains the sender
#  - contains the message received
CHAT_MESSAGE_MESSAGE = 0x51
# when you get banned from chat for whatever reason
#  - reason is given
CHAT_MESSAGE_BANNED = 0x52
# when the server closes while you are in a lobby
#  - when you are in a game you should also get a GAME_STATE_SERVER_SHUTDOWN
CHAT_MESSAGE_SERVER_SHUTDOWN = 0x53
# ate the moment there is no way to check for other chat members,
# in which chat-room you are, etc. 
# There is, however, a rule of thumps:
#  - when you are in a game only your opponent and the spectators can hear you
#  - else all players not in a game can hear you.
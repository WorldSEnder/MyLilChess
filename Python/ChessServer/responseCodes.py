"""
Created on 22.02.2014

@author: Carbon
"""
# informative results, only used if the player polls for 
# the current state etc.. not really used
MOVE_RESULT_INFORMATIVE = 100
# the move was successful
MOVE_RESULT_SUCCESS = 200
MOVE_RESULT_TAKE = 201
MOVE_RESULT_CHECK = 202
MOVE_RESULT_TAKE_CHECK = 203
# there was an error with the MOVE given
MOVE_RESULT_ERROR = 300
MOVE_RESULT_SYNTAX_ERROR = 301
MOVE_RESULT_OUT_OF_BOUNS = 302
MOVE_RESULT_WRONG_MOVE = 303
MOVE_RESULT_NOT_POSSIBLE = 304
MOVE_RESULT_NO_PIECE = 305
MOVE_RESUT_NOT_YOUR_PIECE = 306
# there was an error with the game
MOVE_RESULT_ERROR_GAME = 400
GAME_JOINED = 700
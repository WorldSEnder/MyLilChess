"""
Created on 22.02.2014

@author: WorldSEnder
"""
__author__ = "WorldSEnder"
__version__ = 0.1

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

ordA = ord('a')

def squareToNumber(ident):
    """
    Casts an identifier for squares, like e5, to 
    a number that is the offset in the board-string.
    """
    fileNbr = ord(ident[0]) - ordA
    if fileNbr < 0 or fileNbr > 7:
        raise ValueError("The given identifier doesn't " 
            + "describe a valid fileNbr for of a square: "
            + "Has to be a char from 'a' to 'h'.")
    rank = -1
    try:
        rank = int(ident[1]) - 1
    except ValueError as error:
        raise ValueError("The given identifier doesn't " 
            + "describe a valid fileNbr for of a square: "
            + error)
    if rank < 0 or rank > 7:
        raise ValueError("The given identifier doesn't " 
            + "describe a valid rankNbr for of a square: "
            + "The rank given isn't between 1 and 8.")
    
    return (10 * rank + # simplifies the board
            fileNbr + # plus fileNbr
            21 ) # global offset

def numberToSquare(number):
    fileNbr = (number + 1)%10 - 2 # shortcut, invalid files are now -1 and -2
    rankNbr = (number / 10) # shortcut, valid ranks [1...8]
    if (rankNbr < 1 or
        rankNbr > 8 or
        fileNbr < 0):
        raise ValueError("The number given doesn't describe "
            + "a valid square on the board: " + number)
    return chr(ordA + fileNbr) + str(rankNbr)
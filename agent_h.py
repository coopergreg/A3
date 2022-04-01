"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

dic = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #Terminal State:
    #Use get_score(board) which returns a tuple (number of dark disks, number of light disks)
    
    stuff = get_score(board)
    dark_disk_num = stuff[0]
    light_disk_num = stuff[1]

    if color == 1:
        return dark_disk_num - light_disk_num
    else:
        return light_disk_num - dark_disk_num

    #return 0 #change this!

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    stuff = get_score(board)
    dark_disk_num = stuff[0]
    light_disk_num = stuff[1]

    if color == 1:
        cost = dark_disk_num - light_disk_num
    else:
        cost = light_disk_num - dark_disk_num

    if color == 1:
        new_color = 2
    if color == 2:
        new_color = 1

    corner1 = board[0][0]
    corner2 = board[-1][-1]
    corner3 = board[0][-1]
    corner4 = board[-1][0]

    if corner1 == color:
        cost += 100
    if corner2 == color:
        cost += 100
    if corner3 == color:
        cost += 100
    if corner4 == color:
        cost += 100
    if corner1 == new_color:
        cost -= 100
    if corner2 == new_color:
        cost -= 100
    if corner3 == new_color:
        cost -= 100
    if corner4 == new_color:
        cost -= 100
    '''
    good_len = len(get_possible_moves(board, color))
    bad_len = len(get_possible_moves(board, new_color))
    cost += (good_len - bad_len)
    '''
    return cost
    #return 0 #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0): #For opponent
    #IMPLEMENT (and replace the line below)
    #Ignore limit and caching for now
    #Switch color

    if (caching == 1):
        if (board,color) in dic:
            return dic[(board, color)]

    miny = float("inf")
    if color == 1:
        new_color = 2
    if color == 2:
        new_color = 1

    tup_of_moves = get_possible_moves(board, new_color)

    if tup_of_moves == [] or limit == 0:
        if caching == 1:
            dic[(board, color)] = (None, compute_utility(board, color))
        return (None, compute_utility(board, color)) #We have reached the end, now return the bigg one with the color we had originally
  
    #nice_board = board
    for i in tup_of_moves:
        new_board = play_move(board, new_color, i[0], i[1])
        #Let the max do their thing, with original color
        result = minimax_max_node(new_board, color, limit - 1, caching)[1]
        #Check if result is greater than what we have already done
        if result < miny:
            miny = result
            best_move = i
    if caching == 1:
        dic[(board, color)] = (best_move, miny)
    return (best_move, miny)
    

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT (and replace the line below)
    #We can ignore limit and caching
    #Go down and find the minimum values and pick those
    #play_move(board, color)

    #Check if we have been in this state before
    if (caching == 1):
        if (board,color) in dic:
            return dic[(board, color)]

    maxy = float("-inf")
    tup_of_moves = get_possible_moves(board, color)
    if tup_of_moves == [] or limit == 0:
        if caching == 1:
            dic[(board, color)] = (None, compute_utility(board, color))
        return (None, compute_utility(board, color)) #We have reached the end, now return the bigg one
    
    #nice_board = board
    for i in tup_of_moves:
        new_board = play_move(board, color, i[0], i[1])
        #Let the max do their thing
        result = minimax_min_node(new_board, color, limit - 1, caching)[1]
        #Check if result is greater than what we have already done
        if result > maxy:
            maxy = result
            best_move = i
    if caching == 1:
        dic[(board, color)] = (best_move, maxy)
    return (best_move, maxy)
    

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT (and replace the line below)
    dic = {}
    return minimax_max_node(board, color, limit, caching)[0]

    #return (0,0) #change this!

#def give_me_zero(lol):
#    return lol[0]

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)
    if (caching == 1):
        if (board,color) in dic:
            return dic[(board, color)]
    
    miny = float("inf")
    #Change the color
    if color == 1:
        new_color = 2
    if color == 2:
        new_color = 1

    tup_of_moves = []
    if (ordering == 1):
        #Go through all things in tup of moves
        # = []
        tup_of_moves = sorted(get_possible_moves(board, new_color), key = lambda mo: compute_heuristic(play_move(board, new_color, mo[0], mo[1]), new_color), reverse=True)
        '''
        fat_list = []
        for mo in tup_of_moves:
            new_board = play_move(board, new_color, mo[0], mo[1])
            utility = compute_utility(new_board, color)
            fat_list.append((utility, mo))
        
        
        #So now I have a list of tuples with the third element (index 2) is the and I can sort
        #sort based on compute_utility
        fat_list.sort(key = give_me_zero, reverse = True)
        tup_of_moves = []
        for j in fat_list:
            tup_of_moves.append((j[1][0], j[1][1]))
        '''
    else:
        tup_of_moves = get_possible_moves(board, new_color) 

    if tup_of_moves == [] or limit == 0:
        #We still want the utility for the first player
        if caching == 1:
            dic[(board, color)] = (None, compute_heuristic(board, color))
        return (None, compute_heuristic(board, color)) #We have reached the end, now return the bigg one  

    for i in tup_of_moves:
        new_board = play_move(board, new_color, i[0], i[1])
        
        #Let the max do their thing
        result = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching, ordering)[1]
        #Check if result is greater than what we have already done
        if result < miny:
            miny = result
            best_move = i
        beta = min(beta, miny) #Find minimum of values
        if beta <= alpha:
            #Get out of this, prune it
            break 
    if caching == 1:
        dic[(board, color)] = (best_move, miny)

    return (best_move, miny)

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)

    if (caching == 1):
        if (board,color) in dic:
            return dic[(board, color)]

    maxy = float("-inf")
    
    if (ordering == 1):
        #Go through all things in tup of moves
        # = []
        tup_of_moves = sorted(get_possible_moves(board, color), key = lambda mo: compute_heuristic(play_move(board, color, mo[0], mo[1]), color), reverse=True)
        '''
        fat_list = []
        for mo in tup_of_moves:
            new_board = play_move(board, color, mo[0], mo[1])
            utility = compute_utility(new_board, color)
            fat_list.append((utility, mo))

        
        #So now I have a list of tuples with the third element (index 2) is the and I can sort
        #sort based on compute_utility
        fat_list.sort(key = give_me_zero, reverse = True)
        tup_of_moves = []
        for j in fat_list:
            tup_of_moves.append((j[1][0], j[1][1]))
        '''
    else:
        tup_of_moves = get_possible_moves(board, color)

    if tup_of_moves == [] or limit == 0:
        if caching == 1:
            dic[(board, color)] = (None, compute_heuristic(board, color))

        return (None, compute_heuristic(board, color)) #We have reached the end, now return the bigg one

    #nice_board = board
    for i in tup_of_moves:
        new_board = play_move(board, color, i[0], i[1])
    
        #Let the max do their thing
        result = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)[1]
        #Check if result is greater than what we have already done
        if result > maxy:
            maxy = result
            best_move = i
        #Alpha pruning
        alpha = max(alpha, maxy) #Alpha is the max value
        if beta <= alpha:
            break
    if caching == 1:
        dic[(board, color)] = (best_move, maxy)
    return (best_move, maxy)

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT (and replace the line below)
    dic = {}
    return alphabeta_max_node(board, color, float("-inf"), float("inf"), limit, caching, ordering)[0]

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI_good") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()



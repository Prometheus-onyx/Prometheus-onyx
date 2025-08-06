"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    if x_count > o_count:
        return O
    elif o_count > x_count:
        return X
    else:
        return X  # X starts first
    
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                actions.add((i, j))
    return actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action: Cell already occupied.")
    new_board = copy.deepcopy(board) # Create a copy of the board
    new_board[i][j] = player(board)  # Place the current player's mark
    return new_board

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Check rows and columns
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None  # No winner yet

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True  # No empty cells and no winner means it's a tie

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_ = player(board)
    if winner_ == X:
        return 1
    elif winner_ == O:
        return -1
    else:
        return 0  # Tie or ongoing game
    
    raise NotImplementedError


def minimax(board):

    def Max_Value(board, alpha, beta):
        """
        Returns the maximum value for the current player.
        """
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, Min_Value(result(board, action), alpha, beta))
            alpha = max(alpha, v)
            if v >= beta:
                return v  # Alpha-beta pruning
        return v

    def Min_Value(board, alpha, beta):
        """
        Returns the minimum value for the current player.
        """
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, Max_Value(result(board, action), alpha, beta))
            beta = min(beta, v)
            if v <= alpha:
                return v  # Alpha-beta pruning
        return v

    if player(board) == X:
        best_value = -math.inf
        best_action = None
        alpha = -math.inf
        beta = math.inf
        # Find the best action for X
        for action in actions(board):
            value = Min_Value(result(board, action), alpha, beta)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, best_value)
        return best_action
    else:
        best_value = math.inf
        best_action = None
        alpha = -math.inf
        beta = math.inf
        # Find the best action for O
        for action in actions(board):
            value = Max_Value(result(board, action), alpha, beta)
            if value < best_value:
                best_value = value
                best_action = action
            beta = min(beta, best_value)
        return best_action
        


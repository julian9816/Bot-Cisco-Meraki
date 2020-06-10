"""It will have given the sequence of moves supposing the first move
is always done by X by the numbers of cells where marks are placed
and your task is to determine, at which step the first line was completed
by any side. In this code, a functional solution to this problem is proposed,
which the tic toc toe game poses, but in this case, the 9 movements that can
be performed are placed in a string vector."""

# $ pylint julian9816.py #Linting
# duration: 1.78s
# --------------------------------------------------------------------
# Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
# $python julian9816.py
from typing import List, Any, TextIO


def enter_move(board: List[Any], move: int) -> List[Any]:
    """In this function, the movement to be carried out is received
    as a parameter, an integer between 1 and 9, then X is drawn in
    the box that marks the movement. """

    for i in range(3):
        for j in range(3):
            if board[i][j] == move:
                board[i][j] = "X"
                break
    return board


def victory_for(board: List[Any], sign: str) -> bool:
    """In this function the board receives as a parameter and a
    sign ("O", "X"), so what this function does is define a winner,
    as it is known in this game whoever completes either the diagonals
    or the horizontals with a same symbol be it X or O"""
    if (board[0][0] == sign and board[1][1] == sign and
            board[2][2] == sign):
        winner = True

    elif (board[0][0] == sign and
          board[0][1] == sign and board[0][2] == sign):
        winner = True

    elif (board[1][0] == sign and board[1][1] == sign and
          board[1][2] == sign):
        winner = True

    elif (board[2][0] == sign and board[2][1] == sign and
          board[2][2] == sign):
        winner = True

    elif (board[0][0] == sign and board[1][0] == sign and
          board[2][0] == sign):
        winner = True

    elif (board[0][1] == sign and board[1][1] == sign and
          board[2][1] == sign):
        winner = True

    elif (board[0][2] == sign and board[1][2] == sign and
          board[2][2] == sign):
        winner = True

    elif (board[2][0] == sign and board[1][1] == sign and
          board[0][2] == sign):
        winner = True

    else:
        winner = False

    return winner


def draw_move(board: List[Any], move: int) -> List[Any]:
    """In this function, the movement to be carried out is
     received as a parameter, an integer between 1 and 9,
     and then O is drawn in the box that marks the movement."""
    for i in range(3):
        for j in range(3):
            if board[i][j] == move:
                board[i][j] = "O"
                break
    return board


def movements(moves: str) -> int:
    """In this function it receives the movements in a string vector
    and then separates them after this. What is done is the creation
    of the board which is a 3x3 matrix and each space has a number
    from 1 to 9, after which it is defined that the first element of
    the movement vector is a movement for X and that the second is a
    movement for O and that the third is a movement for X and so on,
    the code stops as soon as it detects a winner and returns the number
    of movements that they made until there was a winner and if there
    is no winner it returns 0"""
    moves_a = moves.split()  # type: List[str]
    board = [[1 for i in range(3)] for i in range(3)]  # type: List[Any]
    num = 1  # type: int
    for i in range(3):
        for j in range(3):
            board[i][j] = num
            num += 1
    for move in range(9):
        if move % 2 == 0:
            board = enter_move(board, int(moves_a[move]))
            winner_x = victory_for(board, "X")  # type: bool
            if winner_x:
                return move + 1
        else:
            board = draw_move(board, int(moves_a[move]))
            winner_o = victory_for(board, "O")  # type: bool
            if winner_o:
                return move + 1
    return 0


def read_file(file: str) -> List[int]:
    """In this function, the DATA.lst file is read,
    the information is extracted and then analyzed."""
    f_readed = open(file, 'r')  # type: TextIO
    content = f_readed.read()  # type: str
    tests = content.splitlines()   # type: List[str]
    results = []   # type: List[int]
    for mov in tests[1:]:
        results.append(movements(mov))
    f_readed.close()
    return results


# $ ./julian9816.py
# $ print(read_file("DATA.lst"))

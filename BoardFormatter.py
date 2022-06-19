from Constants import *


def boardIndexesToPrettyBoardIndexes(i, j):
    index = 0
    superRow = i // 3
    superCol = i % 3
    subRow = j // 3
    subCol = j % 3

    index += 15
    index += superRow * 56
    index += superCol * 4
    index += subRow * 14
    index += subCol
    return index


def prettifyBoard(board):
    formattedBoard = [
        "*", "=", "=", "=", "*", "=", "=", "=", "*", "=", "=", "=", "*", "\n",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", "\n",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", "\n",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", "\n",
        "*", "=", "=", "=", "*", "=", "=", "=", "*", "=", "=", "=", "*", "\n",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", "\n",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", "\n",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", "\n",
        "*", "=", "=", "=", "*", "=", "=", "=", "*", "=", "=", "=", "*", "\n",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", "\n",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", "\n",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", "\n",
        "*", "=", "=", "=", "*", "=", "=", "=", "*", "=", "=", "=", "*", "\n"
    ]
    for i in range(9):
        subBoard = board[i]
        for j in range(9):
            player = subBoard[j]
            if player == PLAYER1:
                symbol = PLAYER1_SYMBOL
            elif player == PLAYER2:
                symbol = PLAYER2_SYMBOL
            else:
                symbol = "."

            index = boardIndexesToPrettyBoardIndexes(i, j)
            formattedBoard[index] = symbol

    return "".join(formattedBoard)


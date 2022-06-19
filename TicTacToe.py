import json
from WinPatterns import WIN_PATTERNS
from BoardFormatter import prettifyBoard
from Constants import *


def convertXYToBoardIndex(x, y):
    index = x + 3 * (2 - y)
    return index


def generateBoard():
    board = []
    for i in range(9):
        board.append(TTTSubBoard(i))
    return board


class TTTSubBoard(list):
    def __init__(self, index):
        super().__init__()
        for i in range(9):
            self.append(BLANK)
        self.winner = 0
        self.index = index


class TTTInstance:

    def __init__(self, prettyBoards):
        self.prettyBoards = prettyBoards
        self.winner = BLANK
        self.superBoard = generateBoard()
        self.currentPlayer = STARTING_PLAYER
        self.currentSubBoard = self.superBoard[CENTER_INDEX]

    def placeSymbol(self, index):
        self.currentSubBoard[index] = self.currentPlayer
        self.checkSubBoardWinCondition()
        self.checkSuperBoardWinCondition()
        self.currentSubBoard = self.superBoard[index]
        self.currentPlayer = self.currentPlayer * -1

    def play(self, x, y):
        index = convertXYToBoardIndex(x, y)
        if self.isCurrentSubBoardFull():
            self.currentSubBoard = self.superBoard[index]
        else:
            self.placeSymbol(index)

    def checkSuperBoardWinCondition(self):
        for pattern in WIN_PATTERNS:
            sumNum = sum(i[0] * i[1].winner for i in zip(pattern, self.superBoard))
            if sumNum == (3 * PLAYER1):
                self.winner = PLAYER1
                break
            elif sumNum == (3 * PLAYER2):
                self.winner = PLAYER2
                break

    def checkSubBoardWinCondition(self):
        for pattern in WIN_PATTERNS:
            sumNum = sum(i[0] * i[1] for i in zip(pattern, self.currentSubBoard))
            if sumNum == (3 * PLAYER1):
                self.currentSubBoard.winner = PLAYER1
                break
            elif sumNum == (3 * PLAYER2):
                self.currentSubBoard.winner = PLAYER2
                break

    def isCurrentSubBoardCellBlank(self, x, y):
        index = convertXYToBoardIndex(x, y)
        return self.currentSubBoard[index] == BLANK

    def isCurrentSubBoardFull(self):
        return all(self.currentSubBoard)

    def hasGameBeenWon(self):
        winner = None
        if self.winner == PLAYER2:
            winner = "Player " + PLAYER2_SYMBOL
        elif self.winner == PLAYER1:
            winner = "Player " + PLAYER1_SYMBOL
        return (self.winner != BLANK), winner

    def getBoard(self):
        if self.prettyBoards:
            board = prettifyBoard(self.superBoard)
        else:
            board = self.superBoard
        return json.dumps([board, self.currentSubBoard.index, self.currentPlayer])

    def close(self):
        self.superBoard = None

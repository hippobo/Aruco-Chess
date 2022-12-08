
from chessboard import display
import sys
import argparse
import os
import numpy as np
import cv2

def ChessToFENNPY(chessBoardStateArray):
    fen_string = 'rnbqkbnr/pppppppp/11111111/11111111/11111111/11111111/PPPPPPPP/RNBQKBNR'

    row1 = [str(v) for v in list(chessBoardStateArray)[0]]
    row2 = [str(v) for v in list(chessBoardStateArray)[1]]
    row3 = [str(v) for v in list(chessBoardStateArray)[2]]
    row4 = [str(v) for v in list(chessBoardStateArray)[3]]
    row5 = [str(v) for v in list(chessBoardStateArray)[4]]
    row6 = [str(v) for v in list(chessBoardStateArray)[5]]
    row7 = [str(v) for v in list(chessBoardStateArray)[6]]
    row8 = [str(v) for v in list(chessBoardStateArray)[7]]

 

    fen_string = ''.join(row1) + '/' + ''.join(row2) + '/' + ''.join(row3) + '/' + ''.join(row4) + '/' + ''.join(row5) + '/' + ''.join(row6) + '/' + ''.join(row7) + '/' + ''.join(row8) 

    return (fen_string )

chess_coords_npy = np.array([["A8","B8","C8","D8","E8","F8","G8","H8"],
["A7","B7","C7","D7","E7","F7","G7","H7"],
["A6","B6","C6","D6","E6","F6","G6","H6"],
["A5","B5","C5","D5","E5","F5","G5","H5"],
["A4","B4","C4","D4","E4","F4","G4","H4"],
["A3","B3","C3","D3","E3","E3","G3","H3"],
["A2","B2","C2","D2","E2","F2","G2","H2"],
["A1","B1","C1","D1","E1","F1","G1","H1"],


])

print(chess_coords_npy[0])

chess_board_state_npy = np.ones((8,8), dtype=object)

chess_board_state_npy[0][1] = 5


print(ChessToFENNPY(chess_board_state_npy))


# game_board = display.start()
# starting_position = 'rnbqkbnr/pppppppp/1p6/8/8/8/PPPPPPPP/RNBQKBNR'
# display.update(starting_position, game_board)


# while True:
#     display.check_for_quit()
#     display.update(starting_position, game_board)


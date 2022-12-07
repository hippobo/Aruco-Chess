
from chessboard import display

game_board = display.start()
starting_position = 'rnbqkbnr/pppppppp/1p6/8/8/8/PPPPPPPP/RNBQKBNR'
display.update(starting_position, game_board)


while True:
    display.check_for_quit()
    display.update(starting_position, game_board)


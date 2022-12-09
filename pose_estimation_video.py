import numpy as np
import cv2
from chessboard import display


CHESS_PIECES = {1 : "NONE", 2 : "R",3 : "N",4 : "B",5 : "Q",6 : "K", 7 : "p", 8 : "r",9 : "n",10 : "b",11 : "q",12 : "k" , 13 : "P"}
cameraMatrix = np.load("calibration_matrix.npy")
distCoeffs = np.load("distortion_coefficients.npy")
transform_matrix = np.load("focus_matrix.npy")

# Constant parameters used in Aruco methods
ARUCO_PARAMETERS = cv2.aruco.DetectorParameters_create()
ARUCO_DICT = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
base_fen_string = 'rnbqkbnr/pppppppp/11111111/11111111/11111111/11111111/PPPPPPPP/RNBQKBNR'



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

    

board = cv2.aruco.GridBoard_create(
        markersX=1,
        markersY=1,
        markerLength=0.02,
        markerSeparation=0.001,
        dictionary=ARUCO_DICT)



#rotation_vectors, translation_vectors, dist = np.load("rvecs.npy"), np.load("tvecs.npy"), np.load('dist.npy')

# Make output image fullscreen
cv2.namedWindow('ChessBoardsImage',cv2.WINDOW_NORMAL)
#cv2.setWindowProperty("ChessBoardsImage", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ret, ChessBoardsImage = cam.read()

ChessBoardsImage = cv2.warpPerspective(ChessBoardsImage, transform_matrix, (1280,720), flags=cv2.INTER_LINEAR)
IMAGE_HEIGHT = ChessBoardsImage.shape[0]
IMAGE_WIDTH = ChessBoardsImage.shape[1]

M = IMAGE_HEIGHT//8
N = IMAGE_WIDTH//8



chess_coords_npy = np.array([
["A8","B8","C8","D8","E8","F8","G8","H8"],
["A7","B7","C7","D7","E7","F7","G7","H7"],
["A6","B6","C6","D6","E6","F6","G6","H6"],
["A5","B5","C5","D5","E5","F5","G5","H5"],
["A4","B4","C4","D4","E4","F4","G4","H4"],
["A3","B3","C3","D3","E3","E3","G3","H3"],
["A2","B2","C2","D2","E2","F2","G2","H2"],
["A1","B1","C1","D1","E1","F1","G1","H1"],
])

chess_board_state_npy = np.ones((8,8), dtype=object)


game_board = display.start()
display.update(ChessToFENNPY(chess_board_state_npy), game_board)


while(cam.isOpened()):
    # Capturing each frame of our video stream
    ret, ChessBoardsImage = cam.read()
    
    
        # grayscale image
    ChessBoardsImage = cv2.warpPerspective(ChessBoardsImage, transform_matrix, (1280,720), flags=cv2.INTER_LINEAR)
    grayImage = cv2.cvtColor(ChessBoardsImage, cv2.COLOR_BGR2GRAY)
   
    y1 = 0
    for y in range(0,IMAGE_HEIGHT,M):
        for x in range(0, IMAGE_WIDTH, N):
            y1 = y + M
            x1 = x + N
            cv2.rectangle(ChessBoardsImage, (x, y), (x1, y1), (0, 255, 0))
            
    if ret:
        # Detect Aruco markers
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(grayImage, ARUCO_DICT, parameters=ARUCO_PARAMETERS)
        #refine detection
        corners, ids, rejectedImgPoints, recoveredIds = cv2.aruco.refineDetectedMarkers(
                image = grayImage,
                board = board,
                detectedCorners = corners,
                detectedIds = ids,
                rejectedCorners = rejectedImgPoints,
                cameraMatrix = cameraMatrix,
                distCoeffs = distCoeffs)   

        if len(corners) > 0:

            chess_board_state_npy = np.ones((8,8), dtype=object)
            
            flat_ids = []
            for sublist in ids:
                for item in sublist:
                    flat_ids.append(item)
            
            
            points = list(zip(flat_ids, corners))
            

            aruco_centers = {}
            for piece_id, corner in points:
                x_chess = int(sum(corner[0][c][0] for c in range(4))/4)//160
                y_chess = int(sum(corner[0][c][1] for c in range(4))/4)//90

                chess_board_state_npy[y_chess, x_chess] = CHESS_PIECES[piece_id] # update for fen string

            cv2.aruco.drawDetectedMarkers(ChessBoardsImage, corners,ids,borderColor=(0, 0, 255)) 
            
        

        
            fen_string = ChessToFENNPY(chess_board_state_npy)
            display.update(fen_string, game_board)

            if (fen_string == base_fen_string):
                cv2.putText(ChessBoardsImage, "Game ready to start !",(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1/2, (0,0,255), 1, cv2.LINE_AA)

        else : 
            chess_board_state_npy = np.ones((8,8), dtype=object)
            fen_string = ChessToFENNPY(chess_board_state_npy)
            display.update(fen_string, game_board)
        cv2.imshow('ChessBoardsImage', ChessBoardsImage)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()


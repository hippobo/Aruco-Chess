import numpy as np
import cv2

cameraMatrix = np.load("calibration_matrix.npy")
distCoeffs = np.load("distortion_coefficients.npy")
transform_matrix = np.load("focus_matrix.npy")

# Constant parameters used in Aruco methods
ARUCO_PARAMETERS = cv2.aruco.DetectorParameters_create()
ARUCO_DICT = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)


board = cv2.aruco.GridBoard_create(
        markersX=1,
        markersY=1,
        markerLength=0.02,
        markerSeparation=0.001,
        dictionary=ARUCO_DICT)


rotation_vectors, translation_vectors, dist = np.load("rvecs.npy"), np.load("tvecs.npy"), np.load('dist.npy')
# axis = np.float32([[-.5,-.5,0], [-.5,.5,0], [.5,.5,0], [.5,-.5,0],
#                    [-.5,-.5,1],[-.5,.5,1],[.5,.5,1],[.5,-.5,1] ])

# Make output image fullscreen
cv2.namedWindow('ChessBoardsImage',cv2.WINDOW_NORMAL)
#cv2.setWindowProperty("ChessBoardsImage", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while(cam.isOpened()):
    # Capturing each frame of our video stream
    # fps = cam.get(cv2.CAP_PROP_FPS)
    # print('frames per second =',fps)
    ret, ChessBoardsImage = cam.read()
    
    if ret == True:
        k = cv2.waitKey(1)
        if k%256 == 32:
        # SPACE pressed
            
            
            
            # grayscale image
            ChessBoardsImage = cv2.warpPerspective(ChessBoardsImage, transform_matrix, (1280,720), flags=cv2.INTER_LINEAR)
            grayImage = cv2.cvtColor(ChessBoardsImage, cv2.COLOR_BGR2GRAY)
            
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
                for i in range(len(ids)):
                    x = (corners[i-1][0][0][0] + corners[i-1][0][1][0] + corners[i-1][0][2][0] + corners[i-1][0][3][0]) / 4
                    y = (corners[i-1][0][0][1] + corners[i-1][0][1][1] + corners[i-1][0][2][1] + corners[i-1][0][3][1]) / 4
                    print("id: ", ids[i])
                    print("y: ", y)
                    print("x: ", x)
                    #rotation_vectors, translation_vectors, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, 1, cameraMatrix, distCoeffs)
                    #FOR WHAT USE??? 
                    cv2.aruco.drawDetectedMarkers(ChessBoardsImage, corners,ids,borderColor=(0, 0, 255)) 

            cv2.imshow('ChessBoardsImage', ChessBoardsImage)


        elif k%256 == 27:
            break

cv2.destroyAllWindows()

#DRAW BOUNDING BOX AROUND CHESSBOARD AND CREATE GRID TO CALCULATE PIECE POSITION
#WAY TO STORE COORDINATES AND FOR EACH PIECE PRESENT RETURN POSITION
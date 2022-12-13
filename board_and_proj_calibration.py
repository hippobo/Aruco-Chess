import cv2
import numpy as np
import math
from itertools import permutations  


screen_coords = [[0,0], [0,720],[1280,0],[1280,720]]
cameraMatrix = np.load("calibration_matrix.npy")
distCoeffs = np.load("distortion_coefficients.npy")
CAM_NUMBER = 0

cv2.namedWindow("Damier", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Damier", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
sleeping_time = 300


def get_frame():

    cap = cv2.VideoCapture(CAM_NUMBER)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    ok, frame = cap.read()

    cap.release()
    
    if not ok:
        cv2.destroyAllWindows()
        print("No camera detected")
        input()
        exit()
    
    return frame

############### place circle with mouseCallBack event ###############

def draw_circle(event,x,y,flags,param):
    # print('x',x,'y',y)
    global l_circle, background
    
    if event in [cv2.EVENT_RBUTTONDOWN, cv2.EVENT_LBUTTONDOWN]:
        
        if len(l_circle)>=4:
            l_circle[min(enumerate([(xC-x)**2+(yC-y)**2 for xC,yC in l_circle]), key=lambda x: x[1])[0]]=[x,y]
        else:
            l_circle+=[[x,y]]
        # print(l_circle)
        frame=background.copy()
        
        for i,p1 in enumerate(l_circle):
            p1=tuple(p1)
            for p2 in l_circle[i+1:]:
                p2=tuple(p2)
                cv2.line(frame,p1,p2,(255,0,0),3)
            cv2.circle(frame,p1,5,(0,0,255),-1)
        
        cv2.imshow('Damier',frame)

        

def ordering(l_point1, l_point2):

    global background
    
    l_distance_ordered=[]
    for l_ordering in permutations(list(range(len(l_point1)))):
        d=0
        l_ordered_point=[]
        for i1,i2 in enumerate(l_ordering):
            d+=np.linalg.norm(np.array(l_point1[i1])
                              - np.array(l_point2[i2]))
            l_ordered_point+=[l_point2[i2]]
        
        l_distance_ordered+=[[d,l_ordered_point]]

    l_ordered_point=min(l_distance_ordered, key=lambda x: x[0])[1]

    frame=background.copy()
    
    for p1,p2 in zip(l_point1, l_ordered_point):
        p1=tuple(p1)
        p2=tuple(p2)
        cv2.line(frame,p1,p2,(255,0,0),3)
        cv2.circle(frame,p1,5,(0,0,255),-1)
        cv2.circle(frame,p2,5,(0,255,0),-1)

    cv2.imshow('Damier',frame)
    cv2.waitKey(2000)
    
    return l_ordered_point

############### Chessboard Calibration ###############

background=get_frame()
cv2.imshow("Damier", background)

cv2.putText(background,
            "Click on chessboard 4 corners",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1/2,
            (0,0,255),
            1,
            cv2.LINE_AA)

l_circle=[]


cv2.setMouseCallback('Damier', draw_circle)

frame=background.copy()
for i,p1 in enumerate(l_circle):
    p1=tuple(p1)
    for p2 in l_circle[i+1:]:
        p2=tuple(p2)
        cv2.line(frame,p1,p2,(255,0,0),3)
    cv2.circle(frame,p1,5,(0,0,255),-1)

cv2.imshow('Damier',frame)

cv2.waitKey(0)
while len(l_circle)<4:
    cv2.waitKey(0)
    
cv2.setMouseCallback('Damier', lambda *args: None)
    
chessboard_coords=l_circle.copy()

frame=background.copy()

chessboard_coords = ordering(screen_coords, chessboard_coords)
 

screen_coords = np.float32(screen_coords)
chessboard_coords = np.float32(chessboard_coords)

focus_matrix = cv2.getPerspectiveTransform(chessboard_coords,screen_coords)

print("CALIBRATION TERMINEE, FOCUS MATRIX CREE")

np.save("focus_matrix",focus_matrix)
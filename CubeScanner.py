#import pandas as pd
import numpy as np
import cv2
from cubesolver import solve_cube
#import matplotlib.pylab as plt

# img_mpl = plt.imread("./CubePhotos/cube1.jpg")

# print(img_mpl.shape)

# fig, ax = plt.subplots(figsize = (20,20))
# ax.imshow(img_mpl)
# ax.axis('off')
# plt.show()

stream = cv2.VideoCapture(0)

if not stream.isOpened():
    print("no stream")
    exit()

streamFPS = stream.get(cv2.CAP_PROP_FPS)

stream.set(cv2.CAP_PROP_AUTO_WB, 0)
stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)

width = int(stream.get(3))
height = int(stream.get(4))

output = cv2.VideoWriter("4_stream.mp4", cv2.VideoWriter_fourcc('m','p','4','v') #codes can be found online and depend on the type of viceo like grayscale or changed bitrate
                        ,fps=streamFPS, frameSize=(width, height))

UserCube = []
sideScanCounter = 0 #this determines which side is being scanned by %6 refer to below
ScanFaceOrder = "URFDLB"
ScanFaceColorName = ["White", "Red", "Green", "Yellow", "Orange", "Blue"]
cubeAnswer = ""

while True:
    ret, frame = stream.read()
    if not ret:
        print("no more stream")
        break

    midWidth, midHeight = width//2, height//2

    fontColor = (110, 108, 125) #cv2 uses BGR
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = frame

    def textCentered(img, text, font, font_scale, fontcolor, thickness, depth):
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

        img = cv2.putText(img, text
                              , (midWidth - text_width//2, depth), font, font_scale, fontcolor, thickness,cv2.LINE_AA) #bottom left hand corner first

    textCentered(img,"Press Q to stop and scan faces by pressing S", font, 0.5, fontColor, 1, 40)
    textCentered(img,"then press fix to solve and R to reset", font, 0.5, fontColor, 1, 60)

    squareSize = 100 # pixels
    lineThickness = 4

    #draw the 9 squares and get the center positions in pixel 
    half = squareSize // 2
    centers = []  # centers[squareX][squareY] -> (cx, cy)

    for squareX in range(3):
        column = []
        for squareY in range(3):
            x1 = int(midWidth  - half * (3 - squareX*2))
            y1 = int(midHeight - half * (3 - squareY*2))
            x2 = int(midWidth  - half * (1-squareX*2))
            y2 = int(midHeight - half * (1-squareY*2))

            img = cv2.rectangle(frame, (x1, y1), (x2, y2),
                        (squareX * 100, 0, squareY * 100), lineThickness)

            column.append(((x1 + x2) // 2, (y1 + y2) // 2))
        centers.append(column)

    #handle detection and storage of cube
    detectedColorsCube = []

    for squareX in range(3):
        column = []
        for squareY in range(3):
            cx = centers[squareX][squareY][0]
            cy = centers[squareX][squareY][1]
            color = frame[cy,cx]

            patch = frame[cy-2:cy+3, cx-2:cx+3]
            b, g, r = patch.mean(axis=(0, 1)).astype(int)
            detectedColorsCube.append((int(b),int(g),int(r)))

    
    detectedColorsCube = [[detectedColorsCube[3*x + y] for x in range(3)] for y in range(3)]

    #URFDLB is the order of the faces detected
    finsihedScan = False
    if sideScanCounter %6 == 0 and sideScanCounter != 0:
        finsihedScan = True

    targetSide = ScanFaceOrder[sideScanCounter%6]
    targetColor = ScanFaceColorName[sideScanCounter%6]
    displayedText = "Scanning for {} / {}".format(targetSide, targetColor)
    fontScale = 1
    if finsihedScan: 
        displayedText = "Scan Completed"
    if cubeAnswer != "":
        fontScale = 0.75
        displayedText = cubeAnswer
    
    textCentered(img, displayedText, font, fontScale, (255,255,255), 1, height - 40)
                
    cv2.resize(frame, (width,height))
    output.write(frame)

    #note that cv2 and mpl have different RGB formats
    cv2.imshow("Webcam!", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'): #press q to stop the streaming
        print("Q hit to stop webcam")
        break

    if key == ord('r'): #press q to stop the streaming
        print("reset")
        UserCube = []
        sideScanCounter = 0
        cubeAnswer = ""

    if key == ord('s'):
        if len(UserCube) == 6:
            print("all faces scanned")
        else:
            # print("The RGBs are")
            cubeFace = []
            for i in range(3):
                # print(detectedColorsCube[i])
                cubeFace.append(detectedColorsCube[i])
            UserCube.append(cubeFace)
            sideScanCounter += 1
            # print(sideScanCounter)

    if key == ord('f'):
        #convert the cube from BGR to LAB first
        def to_lab(bgr):
            return cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2LAB)[0, 0].astype(int)
        UserCubeLab = [[[to_lab(piece) for piece in row] for row in face] for face in UserCube]

        faceCentersLAB = {}
        for i in range(6):
            faceCentersLAB[ScanFaceOrder[i]] = UserCubeLab[i][1][1]

        #match every piece to the closest LAB color
        def closestColorLab(lab_val):
            return min(faceCentersLAB, key=lambda n: np.sum((faceCentersLAB[n] - lab_val)**2))

        cubeDefinitionString = ""
        for face in UserCubeLab:
            for row in face:
                for piece in row:
                    cubeDefinitionString += closestColorLab(piece)

        print()
        print(cubeDefinitionString)
        print()
        cubeAnswer = solve_cube(cubeDefinitionString)
        print(cubeAnswer)
            

stream.release()
cv2.destroyAllWindows()

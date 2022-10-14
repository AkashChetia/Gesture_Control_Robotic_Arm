import time
from time import sleep
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.SerialModule import SerialObject

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2, detectionCon=0.7)

mySerial = SerialObject("ACM0", 9600, 1)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    # For one hand detection either left or right
    if hands:
        if hands[0] and len(hands) == 1:
            hand1 = hands[0]
            print(hand1['type'])
            print("\nNO. OF HANDS: ", len(hands))

            fingers1 = detector.fingersUp(hand1)
            print("fingers count: ", fingers1.count(1))
            mySerial.sendData(fingers1)
            print(fingers1)

            # if fingers1.count(1):

            font = cv2.FONT_HERSHEY_SIMPLEX

            # org
            org = (50, 50)

            # fontScale
            fontScale = 0.8

            # Blue color in BGR
            color = (153, 0, 0)

            # Line thickness of 2 px
            thickness = 2

            # Using cv2.putText() method to print text on img at real time
            img = cv2.resize(img, (900, 540))  # windows size adjustment while hand is detected
            img = cv2.putText(img, (hand1['type'] + " " + " [ " + " ".join(str(x) for x in fingers1) + " ] "), org, font,
                              fontScale, color, thickness, cv2.LINE_AA)

        elif hands[1] and len(hands) == 1:
            hand2 = hands[1]
            print("\nNO. OF HANDS: ", len(hands))

            fingers2 = detector.fingersUp(hand2)
            print("fingers count: ", fingers2.count(1))
            mySerial.sendData(fingers2)
            print(fingers2)

            # if fingers2.count(1):
            font = cv2.FONT_HERSHEY_SIMPLEX

            # org
            org = (50, 50)

            # fontScale
            fontScale = 0.8

            # Blue color in BGR
            color = (153, 0, 0)

            # Line thickness of 2 px
            thickness = 2

            # Using cv2.putText() method  to print text on img at real time
            img = cv2.resize(img, (900, 540))  # windows size adjustment while hand is detected
            img = cv2.putText(img, (hand2['type'] + " " + " [ " + " ".join(str(x) for x in fingers2) + " ] "), org, font,
                              fontScale, color, thickness, cv2.LINE_AA)

    # For both hands detection concurrently
    if len(hands) == 2:
        hand2 = hands[1]
        hand1 = hands[0]
        print("\nNO. OF HANDS: ", len(hands))

        print("\nNO. OF HANDS: ", len(hands))

        fingers1 = detector.fingersUp(hand1)

        fingers2 = detector.fingersUp(hand2)
        mySerial.sendData(fingers1)
        mySerial.sendData(fingers2)
        print(fingers1, fingers2)

        # if fingers2.count(1):
        font = cv2.FONT_HERSHEY_SIMPLEX

        # org
        org = (50, 50)

        # fontScale
        fontScale = 0.7

        # Blue color in BGR
        color = (153, 0, 0)

        # Line thickness of 2 px
        thickness = 2

        # Using cv2.putText() method
        img = cv2.resize(img, (1000, 700))
        img = cv2.putText(img, (hand1['type'] + " [ " + " ".join(str(x) for x in fingers1) + "] " + hand2['type'] + " [ " + " ".join(
            str(y) for y in fingers2) + "] "), org, font,
                          fontScale, color, thickness, cv2.LINE_AA)

        if(fingers1.count(0) + fingers2.count(0)) == 10:
            # Gap
            t_end = time.time() + 1 * 1
            while time.time() < t_end:
                img = cv2.putText(img, "BYE!", (-6, 500), font,
                                  7, (0, 0, 255), thickness, cv2.LINE_AA)

            detector = None

    cv2.imshow("Image", img)

    cv2.waitKey(1)




































import cv2
import numpy as np
import utlis

##############################################################################
#
# cameraNo = 1
# portNo = "COM4"
# cropVals = 100, 100, 300, 400  # StartPointY StartPointX h w
# frameWidth = 640
# frameHeight = 480
# brightnessImage = 230
#
#
#
#
# ##############################################################################
#
# cap = cv2.VideoCapture(-1, cv2.CAP_V4L)
# cap.set(10, brightnessImage)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
# utlis.initializeTrackBar()
# utlis.connectToRobot(portNo)
#
#
#
#
# while True:
#     success, img = cap.read()
#     if img is None:
#         break
#     imgResult = img.copy()
#
#     imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
#     imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
#     trackBarPos = utlis.getTrackbarValues()
#     imgMask, imgColorFilter = utlis.colorFilter(imgHSV, trackBarPos)
#
#     imgCropped = imgMask[cropVals[1]:cropVals[2] + cropVals[1], cropVals[0]:cropVals[0] + cropVals[3]]
#     imgResult = imgResult[cropVals[1]:cropVals[2] + cropVals[1], cropVals[0]:cropVals[0] + cropVals[3]]
#     imgOpen = cv2.morphologyEx(imgCropped, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
#     imgClosed = cv2.morphologyEx(imgOpen, cv2.MORPH_CLOSE, np.ones((10, 10), np.uint8))
#     imgFilter = cv2.bilateralFilter(imgClosed, 5, 75, 75)
#     imgContour, imgResult = utlis.getContours(imgFilter, imgResult)
#
#     ## TO DISPLAY
#     cv2.rectangle(img, (cropVals[0], cropVals[1]), (cropVals[0] + cropVals[3], cropVals[2] + cropVals[1]), (0, 255, 0),
#                   2)
#     stackedImage = utlis.stackImages(0.7, ([img, imgMask, imgColorFilter], [imgCropped, imgContour, imgResult]))
#
#     # imgBlank = np.zeros((512, 512, 3), np.uint8)
#     # stackedImage = utlis.stackImages(0.7, ([img, imgBlank, imgBlank], [imgBlank, imgBlank, imgBlank]))
#
#     cv2.imshow('Stacked Images', stackedImage)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

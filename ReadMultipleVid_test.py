



import cv2
import os
import CommonWild_2 as C


vidNum = 0
for vid in os.listdir(C.FOLDER):
    if vid.endswith(".mp4"):
        vidNum += 1
        print ('hi from vid', vidNum)
        vidPath = os.path.join(C.FOLDER, vid)
        cap = cv2.VideoCapture(vidPath)
        cap.set(cv2.CAP_PROP_POS_FRAMES, C.START_FRAME)
        frameCount = C.START_FRAME    # keep video reader and object processing in sync
        while(cap.isOpened()):  # start frame capture
            print (frameCount)
            if frameCount > C.MAX_FRAME: # end processing if reaches max frame (in case request to process partial video)
                break
            ret, colorIM = cap.read()
            frameCount += 1           # increment frame counter
                
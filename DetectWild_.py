



import numpy as np
import cv2
import glob
import CommonWild_1 as C
import FeatureWild_1 as F

# Rather than processing a video, DetectTrackFeature code was modified to process all images in a desired directory
# For this reason, tracking and debug display code were excluded

######### FUNCTIONS #############

def imageProcessing(colorIM):
    grayIM = cv2.cvtColor(colorIM, cv2.COLOR_BGR2GRAY)     # convert color to grayscale image
    blurIM = cv2.medianBlur(grayIM, C.BLUR)                # blur image to fill in holes to make solid object
    ret,threshIM = cv2.threshold(blurIM, C.THRESH,255, cv2.THRESH_BINARY_INV) # threshold image to make pixels 0 or 255
    contourList, hierarchy = cv2.findContours(threshIM, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # all countour points, uses more memory
    return(grayIM, threshIM, blurIM, contourList)


def checkROI(xMaxRez, yMaxRez, xx0, yy0, xx1, yy1):
    xx0 -= C.ENLARGE     # enlarge region of interest
    yy0 -= C.ENLARGE 
    xx1 += C.ENLARGE
    yy1 += C.ENLARGE
    touch = 0         	 # assume enlarged ROI does not touch image boundary
    x0 = max(xx0, 0)     # check that enlarged is still in frame
    x1 = min(xx1, xMaxRez) 
    y0 = max(yy0, 0)
    y1 = min(yy1, yMaxRez)
    print (x0, x1, y0, y1)
    if x0 != xx0 or x1 != xx1 or y0 != yy0 or y1 != yy1: # if changed any, report touched image boundary
        touch = 1
    return(touch, x0, y0, x1, y1)


def maskIM(colorIM, threshIM, cnt, x0, y0, x1, y1):
    blackIM = np.zeros_like(threshIM)
    cv2.drawContours(blackIM, [cnt], -1, 255, -1) # function takes array of arrays so need [objContour] !!!
    binaryROI = blackIM[y0:y1,x0:x1]
    colorROI = colorIM[y0:y1,x0:x1]
    colorROI = cv2.bitwise_and(colorROI,colorROI,mask = binaryROI)
    grayROI = cv2.cvtColor(colorROI, cv2.COLOR_BGR2GRAY)     # convert colorROI to grayscale image
    return(colorROI, grayROI, binaryROI)


def DetectFeature(FOLDER):
    status = 0 # return status, 1=good (found and processed image)
    # create objectArray to store objectArray+featureVector
    objectArray = np.zeros((0, C.MAX_OBJ_COL), dtype='float') # array of all objects for all frames
    objectArrayZero = np.zeros((1, C.MAX_OBJ_COL), dtype='float') # one row filled with zeros to append at beginning of loop
    oi = 0    # object index, points into objectArray
    imCount = 0
    for img in glob.glob(FOLDER):
        colorIM = cv2.imread(img)
        imCount += 1
        #print (imCount, colorIM.shape, ' image read')
        (yColorIM, xColorIM, color) = colorIM.shape
        rectIM = np.copy(colorIM) 	# make copy that can be marked up with rectangles
        (grayIM, threshIM, blurIM, contourList) = imageProcessing(colorIM) 	# do image processing

        goodObjCount = 0  # counts number of objects of acceptable area and no touch
        for objContour in contourList:
            area = cv2.contourArea(objContour)
            if area > C.MIN_AREA:
                PO = cv2.boundingRect(objContour) # get bounding box for ROI
                x0 = PO[0]
                y0 = PO[1]
                x1 = x0 + PO[2]
                y1 = y0 + PO[3]
                xc = x0 + (x0 + x1) / 2
                yc = y0 + (y0 + y1) / 2
                (touch, x0, y0, x1, y1) = checkROI(xColorIM, yColorIM, x0, y0, x1, y1) # return 1 if object touches image boundary
                if area > C.MAX_AREA:
                    print('touch',touch,'area',area,'len(contourList)',len(contourList))
                if area > C.MIN_AREA and area < C.MAX_AREA:    # only process assigned species objects of good size that don't touch image edge
                    print ('hi from image:', imCount, 'oi:', oi)
                    goodObjCount += 1     
                    # Get ROI using a mask to eliminate everything in the ROI except the object
                    (colorROI, grayROI, binaryROI) = maskIM(colorIM, threshIM, objContour, x0, y0, x1, y1) # mask images using contour to eliminate any other objects in ROI
                    cv2.rectangle(rectIM, (x0, y0), (x1, y1), (255, 255, 0), C.THICK)   # draw blue/green rectangle around good object
                    cv2.imshow('rectIM', cv2.resize(rectIM,(C.X_REZ_DEBUG, C.Y_REZ_DEBUG))) # display object with rectangle
                    cv2.imshow('binaryROI', cv2.resize(binaryROI,(C.X_REZ_DEBUG, C.Y_REZ_DEBUG)))
                    cv2.imshow('threshIM', cv2.resize(threshIM,(C.X_REZ_DEBUG, C.Y_REZ_DEBUG)))
                    cv2.moveWindow('binaryROI', 640, -200)
                    cv2.moveWindow('threshIM', 640, 400)
                    cv2.waitKey(3000) # pause for 3 seconds before fetching next image
                    # add a row of zeros and assign columns to obj variables
                    objectArray = np.append(objectArray, objectArrayZero, axis = 0)  # append empty row to objectArray, then fill with values 
                    objectArray[oi, C.IMCOUNT] = imCount
                    objectArray[oi, C.X0 : C.YC + 1] = (x0, y0, x1, y1, xc, yc)
                    objectArray[oi, C.AREA] = area                 
                    # Get object features, add to objectArray, then append objectArray to objectArray
                    featureVector = F.getFeatures(grayROI, binaryROI, objContour)
                    objectArray[oi, C.FEATURE_START : C.FEATURE_END] = featureVector
                    oi += 1  # end of processing object so increment obj index
        status = 1 # indicates that program is reading images successfully
    return (status, objectArray)

########### TEST ###############

if False:
    folder = "/users/anthonybravo/Desktop/SFSU/CSC667_opticalEngineering/video/merced/9am_holo/*.jpg"
    objFile = 'test.csv'
    print('Processing')
    (status, objectArray) = DetectFeature(folder)
    np.savetxt(objFile, objectArray, header = C.header, fmt = '%f', delimiter = ',') # saves numpy array as a csv file  

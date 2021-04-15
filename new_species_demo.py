


########### IMPORTS ############

import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

###### CONSTANTS/SETTINGS #######

VIDEO = r'planktonVariety.mp4'
# set feature array and output file	
FRAME = 0; ID = 1; CLUSTER = 1; X0 = 2; Y0 = 3; X1 = 4; Y1 = 5; AREA = 6; ASPECT_RATIO = 7; TEXTURE = 8; SOLIDITY = 9; AVG_BRIGHTNESS = 10  
FEATURE_COUNT = 11
featureArray = np.empty((0, FEATURE_COUNT))
OUTPUT_FILE_NAME = 'planktonFeatures.csv'
HEADER_NAME = 'framecount, objcount, x0, y0, x1, y1, area, aspect_ratio, texture, solidity, brightness'
# image specs
X_REZ = 640
Y_REZ = 480
THRESH = 100
BLUR = 7
THICK = 2
MIN_AREA = 300  
CLUSTER_HEADER = 'frame,cluster,x0,y0,x1,y1,area,aspectRatio,texture,solidity, brightness'     
CLUSTER_OUTPUT_FILE_NAME = r'planktonClusters.csv' 
                   
########## FUNCTIONS ############

def getTexture(grayROI):
	edgeROI = cv2.Canny(grayROI, 100, 200)
	onPixels = np.sum(edgeROI) / 255
	w, h = grayROI.shape
	roi_area = w * h
	texture = onPixels / roi_area
	edgeROI_resized = cv2.resize(edgeROI, (320, 240))
	cv2.imshow('edgeROI', edgeROI_resized)
	cv2.moveWindow('edgeROI', 000, 550)
	return texture


def getFeatures(framecount, objcount, obj, colorROI, grayROI, threshROI, x0, y0, x1, y1):
	# get object area
	area = cv2.contourArea(obj)
	# get aspect ratio >= 1 using the minumum area rectangle
	rect_area = cv2.minAreaRect(obj)	
	cx, cy = rect_area[0]
	w, h = rect_area[1]
	if w == 0 or h == 0:
		aspect_ratio = 0
	elif w >= h:
		aspect_ratio = w / h
	else:
		aspect_ratio = h / w
	# get extent
	extent = area / (w * h)
	# get solidity
	hull = cv2.convexHull(obj)
	hull_area = cv2.contourArea(hull)
	solidity = area / hull_area
	# get equivilant diameter
	equi_diameter = np.sqrt(4 * area / np.pi)
	# get mean intensity color ratios -- no need to sum (B, G, R) if each one has its own independent intensity from 0 - 255
	mean_colors = cv2.mean(obj)
	B = mean_colors[0]
	G = mean_colors[1]
	R = mean_colors[2]
	BtoG = B / G
	RtoG = R / G
	#get average brightness
	brightness = int(0)
	# get texture 
	texture = getTexture(grayROI)
	# return a vector with all features	
	featureVector = np.array([[framecount, objcount, x0, y0, x1, y1, area, aspect_ratio, texture, solidity, brightness]])
	return featureVector


def processVideo(VIDEO): 

	global featureArray

	# start capturing frames of video from 0
	cap = cv2.VideoCapture(VIDEO)
	framecount = 0
	
	while(cap.isOpened()):
		# wait 1ms; quit if key 'q' is pressed
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break
		# get/read frame image
		ret, frameIM = cap.read()
		if not ret:
			print('cannot find video or all done')
			break
		# crop out border to avoid capturing full frame contours
		frameIM = frameIM[10:-10, 10:-10, :]
		# reduce to VGA ; make a VGA copy
		vgaIM = cv2.resize(frameIM, (X_REZ, Y_REZ))
		vga2IM = np.copy(vgaIM)
		# gray colored image; blur; thresh
		grayIM = cv2.cvtColor(vgaIM, cv2.COLOR_BGR2GRAY)
		blurIM = cv2.medianBlur(grayIM, BLUR)
		ret, threshIM = cv2.threshold(grayIM, THRESH, 255, cv2.THRESH_BINARY_INV)
		# get all contours of outermost objects only 
		contourList, hierarchy = cv2.findContours(threshIM, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

		objcount = 0
		for obj in contourList:		
			# compute object area
			area = cv2.contourArea(obj)
			if area > MIN_AREA:
				# increase object count
				objcount += 1
				# get straight bounding rectangle coordinates
				PO = cv2.boundingRect(obj)
				x0 = PO[0]
				y0 = PO[1]			
				x1 = x0 + PO[2]
				y1 = y0 + PO[3]
				# draw BG straight bounding rectangle 
				cv2.rectangle(vgaIM, (x0, y0), (x1, y1), (255, 255, 0), THICK)
				# get minimum area rectangle coordinates
				rect_area = cv2.minAreaRect(obj)
				box = cv2.boxPoints(rect_area)
				box = np.int0(box)
				# draw BR minimum area rectangle 
				cv2.drawContours(vgaIM, [box], 0, (255, 0, 255), 2)
				# crop ROIs
				colorROI = vga2IM[y0:y1, x0:x1, :]
				grayROI = grayIM[y0:y1, x0:x1]
				threshROI = threshIM[y0:y1, x0:x1]
				# call feature function ; append feature array with object feature vector
				objFeatures = getFeatures(framecount, objcount, obj, colorROI, grayROI, threshROI, x0, y0, x1, y1)
				featureArray = np.append(featureArray, objFeatures, axis = 0)
				fv = objFeatures[0]
				# if True:  --- Tom had this if statement in his code before print. What's it's purpose? I get the same result either way.
				print('frame:', int(fv[0]), 'objNum:', int(fv[1]), 'x0:', int(fv[2]), 'y0:', round(fv[3], 1), 'x1:', round(fv[4], 2), 'y1:', round(fv[5], 2) , 'area:', round(fv[6], 2) , 'aspect_ratio:', round(fv[7], 2), 'texture:', round(fv[8], 2), 'solidity:', round(fv[9], 2), 'brightness:', round(fv[10], 2))
				# quick check that .csv file actually saves
				if framecount == 2:
					np.savetxt(OUTPUT_FILE_NAME, featureArray, header = HEADER_NAME, fmt = '%f', delimiter = ',')
		framecount += 1
		#show results
		cv2.imshow('vgaIM', vgaIM)
		cv2.imshow('threshIM', threshIM)
		cv2.moveWindow('vgaIM', 000, 000)
		cv2.moveWindow('threshIM', 650, 000)
	if framecount > 1:
		print('Done with video')
		np.savetxt(OUTPUT_FILE_NAME, featureArray, header = HEADER_NAME, fmt = '%f', delimiter = ',')
		print ('Feature file saved, goodbye!')
	else:
		print('Error: Cannot find video:', VIDEO, 'Ending program.')
	    
	cap.release()
	cv2.destroyAllWindows()
	return

def doCluster(XT, i):
    
    K = KMeans(n_clusters = i)       			# initiate the k means estimator
    K.fit(XT)                             		# Compute k-means clustering
    predict = K.fit_predict(XT)           		# Predict the closest cluster each sample in X belongs to.
    inertia = K.inertia_
    iterations = K.n_iter_
    scaledInertia = int(inertia/1000000)  		# inertia is a big floating point number, so scale for easy reading when displayed 
    INERTIA.append(scaledInertia)				# append INERTIA list with new scaled inertia for each cluster
    print ('clusters', i, 'inertia',scaledInertia, 'iterations', iterations)   
    return

######### MAIN ###########

processVideo(VIDEO)

featureFile = np.loadtxt(OUTPUT_FILE_NAME, skiprows=1, delimiter=',')
print('Loaded', OUTPUT_FILE_NAME, 'Shape', featureFile.shape)
XT = featureFile[:, AREA:]
# list of amount of clusters to try
clusterList = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] 
INERTIA=[] 

for i in clusterList:
	doCluster(XT, i)

plt.plot(clusterList, INERTIA)
plt.xlabel("clusters")
plt.ylabel("inertia")
plt.title("inertia v. clusters")
plt.show()



import DetectWild_2 as D
import ClusterWild_2 as K
import CommonWild_2 as C # constants used by all programs
import numpy as np
import os
import matplotlib.pyplot as plt

for vid in os.listdir(C.FOLDER):
    if vid.endswith(".mp4"):
        print('Processing', vid)
        vidPath = os.path.join(C.FOLDER, vid)
        (status,objectArray) = D.detectTrackFeature(vidPath) # status==1 if processed video
        if status == 1:
            for i in K.clusterList:
                (objectArray,inertia,iterations) = K.cluster(objectArray, i)
            
            inertiaArray = np.array(K.INERTIA)
            plt.plot(K.clusterArray, inertiaArray)
            plt.xlabel("clusters")
            plt.ylabel("inertia")
            plt.title("inertia v. clusters")
            plt.show()
                
            clusterNum = int(input("enter number of clusters at elbow: "))
            (objectArray,inertia,iterations) = K.cluster(objectArray, clusterNum)
            np.savetxt(vid[:-5] + 'Features',objectArray,header = C.header,fmt = '%f',delimiter = ',') # saves numpy array as a csv file    
    

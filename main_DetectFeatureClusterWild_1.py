



import numpy as np
import CommonWild_1 as C # constants used by all programs
import DetectWild_1 as D
import ClusterWild_1 as K
import matplotlib.pyplot as plt

print('Processing',C.FOLDER)
(status,objectArray)=D.DetectFeature(C.FOLDER) # status==1 if processed video
objectArray = D.getPCA(objectArray)                            #for main_detectfeature code
if status==1:
    clusterList = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # list of amount of clusters to try
    for i in clusterList:
        (objectArray,inertia,iterations)=K.Cluster(objectArray, i)
        print('clusters:', i,'inertia:',inertia,'iterations',iterations)
            
    
    plt.plot(clusterList, K.INERTIA)
    plt.xlabel("clusters")
    plt.ylabel("inertia")
    plt.title("inertia v. clusters")
    plt.show()

    clusterNum = int(input("enter number of clusters at elbow: "))
    (objectArray,inertia,iterations) = K.Cluster(objectArray, clusterNum)
    np.savetxt(C.OBJECT_ARRAY_FILE_NAME,objectArray,header=C.header,fmt='%f',delimiter=',') # saves numpy array as a csv file
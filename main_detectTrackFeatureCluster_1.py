import Detect_9 as D
import Cluster_8 as K
import Common_4 as C # constants used by all programs
import numpy as np

print('Processing',C.VID_FILE_NAME)
(status,objectArray)=D.detectTrackFeature(C.VID_FILE_NAME) # status==1 if processed video
if status==1:
    (objectArray,inertia,iterations)=K.cluster(objectArray)
    print('clusters',C.N_CLUSTERS,'inertia',inertia,'iterations',iterations)
    np.savetxt(C.OBJECT_ARRAY_FILE_NAME,objectArray,header=C.header,fmt='%f',delimiter=',') # saves numpy array as a csv file    
    

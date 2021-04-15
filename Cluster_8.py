# Clustering using K-Means
# Clusters objects in feature space using K-means
# See https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans.get_params
#
# V8 Nov 4, 2020 Use common constants, put in module form
# V6 Oct 7, 2020 Removed unnecessary code from doCluster()
# V5 Oct 5, 2020 Consolobjectated code into one program
#
# Tom Zimmerman, IBM Research
# This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction. Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.

from sklearn.cluster import KMeans
import numpy as np
import Common_4 as C # constants used by all programs

#################### FUNCTIONS ###########################

def cluster(objectArray):

    # Cluster and put cluster group into obj file as predicted class
    XT=objectArray[:,C.FEATURE_START:]
    K=KMeans(n_clusters=C.N_CLUSTERS)       # initiate the k means estimator
    K.fit(XT)                           # Compute k-means clustering

    # Predict cluster using K-mean on features
    predict=K.fit_predict(XT)           # Predict the closest cluster each sample in X belongs to.
    inertia=K.inertia_
    iterations=K.n_iter_
    scaledInertia=int(inertia/1000)  # inertia is a big floating point number, so scale for easy reading when displayed 
    objectArray[:,C.CLUSTER]=predict[:] # assign cluster to predicted class

    return(objectArray,scaledInertia,iterations)

####################### MAIN ########################

# load object file
#objectFile=np.loadtxt(OBJECT_FILE_NAME,skiprows=1,delimiter=',')
#print('Loaded',OBJECT_FILE_NAME,'Shape',objectFile.shape)



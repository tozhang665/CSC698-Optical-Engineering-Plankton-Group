# User defined files
VID_FILE_NAME = r'planktonVariety.mp4'
OBJECT_ARRAY_FILE_NAME = 'dil_ab.csv'


# Video processing
MAX_FRAME = 1012        	  # # dil species starts at frame 742 (this will be the new 0) and ends at after frame 1012. this makes a total of 271 frames to process. number of frames to process, make really big to process entire movie
START_FRAME = 742
DEBUG = 1                 # shows detection and tracking frame-by-frame (but slows down processing)
X_REZ_DEBUG = 640
Y_REZ_DEBUG = 480  		  # debug display
THICK = 3                 # ROI box line thickness

# Detector 
THRESH = 100
BLUR = 7
MIN_AREA = 2600
MAX_AREA = 15000
ENLARGE = 10              # increase ROI to include all of obj, also used to detect if near boarder or other objects in ROI window
MULTI_OBJECT_REJECT = 0   # 1 = reject obj with multiple objects in ROI
MIN_OBJ_LEN = 100         # file must have at least this many objets else it is not processed

# tracker
MAX_MATCH_DISTANCE = 100  # obj must be this close or better to track ID, couold be as low as 20 based on analysis
MAX_DELTA_AREA = 0.2      # tracker won't match with object if caused large percent change in area

# speed
SPEED_WINDOW = 10
MIN_SPEED = 10            # objects slower than this are rejected

# Clustering
PCA_COMPONENTS = 3        # how many PCA components
N_CLUSTERS = 5            # how many K Means clusters

# feature 
MAX_FEATURES = 68 		  # number of features getFeatures returns. Area is the first feature

# obj file header and index pointers
header = 'frame,trackID,cluster,clusterReject,class,classReject,x0,y0,x1,y1,xc,yc,trackDistance,deltaArea,speed,area,aspectRatio,texture,solidity,eMajor,eMinor,contourLen,perimeter,radius,mean,std'

# detection and feature column pointers
FRAME = 0; TRACK_ID = 1; CLUSTER = 2; CLUSTER_REJECT = 3; CLASS = 4; CLASS_REJECT = 5; X0 = 6; Y0 = 7; 
X1 = 8; Y1 = 9; XC = 10; YC = 11; TRACK_DISTANCE = 12; DELTA_AREA = 13; SPEED = 14; MAX_OBJECT_VECTOR = 15

MAX_FEATURE_VECTOR = 68           # number of features Feature function returns
FEATURE_START = MAX_OBJECT_VECTOR
FS = FEATURE_START                # FS is an abbreviation so I don't have to keep writing this big constant name
AREA = FS
ASPECT_RATIO = FS+1; TEXTURE = FS+2; SOLIDITY = FS+3; E_MAJOR = FS+4; E_MINOR = FS+5; CONTOUR_LEN = FS+6
PERIMETER = FS+7; RADIUS = FS+8; MEAN = FS+9; STD = FS+10; FEATURE_END = FS+MAX_FEATURE_VECTOR
PCA_1 = FEATURE_END+1; PCA_2 = PCA_1+1; PCA_3 = PCA_2+1; MAX_OBJ_COL = PCA_3+1 
#OBJECT_ARRAY_COL=MAX_OBJECT_VECTOR+MAX_FEATURE_VECTOR # how many col in objectArray


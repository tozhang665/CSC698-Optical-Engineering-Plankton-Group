"""
findZ_6.jpg 
V6 2.23.21 image format= did_13_3940.jpg where 13 is image number, Z in um, if z=0, no focus is provided

Use SPACE BAR to save z in file name.
Use 'x' to skip file
Use 'q' to quit
"""
import numpy as np
import cv2
from os import listdir,rename
from os.path import isfile, join

################## SETTINGS ################
defaultZ=3000 # if z is not known
zStep = 10 # how many Z values to traverse at a time.
dxy   = 1.4e-6 # imager pixel size in meters.
wvlen = 650.0e-9 # Red 
#wvlen = 405.0e-9 # Blue 
zScale=1e-6 # convert z units to microns 
DISPLAY_REZ=(800,800)  

dirIn = r'C:\Code\A_PINC_SFSU\Spring2021\code\findZ\holoImage\\'
dirOut=dirIn
################# FUNCTIONS #################

def recoFrame(cropIM, z):
    #make even coordinates
    (yRez,xRez)=cropIM.shape
    if (xRez%2)==1:
        xRez-=1
    if (yRez%2)==1:
        yRez-=1
    cropIM=cropIM[0:yRez,0:xRez]
    complex = propagate(np.sqrt(cropIM), wvlen, z, dxy)	 #calculate wavefront at z
    amp = np.abs(complex)**2          # output is the complex field, still need to compute intensity via abs(res)**2
    ampInt = amp.astype('uint8')
    return(ampInt, complex)

def propagate(input_img, wvlen, zdist, dxy):
    M, N = input_img.shape # get image size, rows M, columns N, they must be even numbers!

    # prepare grid in frequency space with origin at 0,0
    _x1 = np.arange(0,N/2)
    _x2 = np.arange(N/2,0,-1)
    _y1 = np.arange(0,M/2)
    _y2 = np.arange(M/2,0,-1)
    _x  = np.concatenate([_x1, _x2])
    _y  = np.concatenate([_y1, _y2])
    x, y  = np.meshgrid(_x, _y)
    kx,ky = x / (dxy * N), y / (dxy * M)
    kxy2  = (kx * kx) + (ky * ky)

    # compute FT at z=0
    E0 = np.fft.fft2(np.fft.fftshift(input_img))

    # compute phase aberration
    _ph_abbr   = np.exp(-1j * np.pi * wvlen * zdist * kxy2)
    output_img = np.fft.ifftshift(np.fft.ifft2(E0 * _ph_abbr))
    return output_img

##############  MAIN  ##############

# find files in directory
files = [f for f in listdir(dirIn) if isfile(join(dirIn, f))]
startIndex=0
for i in range(startIndex,len(files)):
    fileName=files[i]
    print(fileName)
    
    # create fileIndex from fileName
    # file format did_13_3940.jpg
    a=fileName.split('_')
    b=a[2].split('.')
    fileIndex=int(a[1])
    z=int(b[0])
    if z==0:
        z=defaultZ
    #print(fileName,fileIndex,z)

    # get image
    im = cv2.imread(dirIn + fileName, 0) #Read the image as grayscale.              
    #cv2.imshow('rawIM',cv2.resize(im,DISPLAY_REZ))

    count=0
    done=False
    end=False
    reject=False
    while done==False and end==False:
        (ampIM, complexIM) = recoFrame(im, z*zScale)
        cv2.imshow('reco',cv2.resize(ampIM,DISPLAY_REZ))
        key=cv2.waitKey(1)
        if key==ord(' '): #space bar SAVE GOOD X
            done=True
        elif key==ord('='): 
            z+=zStep
        elif key==ord('+'): 
            z+=zStep*10
            print(z,end=',')
        elif key==ord('-'): 
            z-=zStep
        elif key==ord('_'): 
            z-=zStep*10
            print(z,end=',')
        elif key== ord('q'):
            end=True
        elif key==ord('x'):
            done=True
            reject=True
        
    if end==True:
        break
    elif reject==True:
        pass
    elif done==True:
        newName=a[0]+'_'+str(a[1])+'_'+str(z)+'.jpg'
        print(fileIndex,fileName,z,newName)
        rename(dirIn+fileName,dirOut+newName)
        
print('Quit requested so closing window and ending program, bye!')
cv2.destroyAllWindows()

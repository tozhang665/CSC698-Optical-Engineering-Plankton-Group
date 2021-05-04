# Interactive Holographic Reconstruction with Tkinter interface
# Tom Zimmerman, IBM Research
# Holgraphic Reconstruction Algorithms by Nick Antipac, UC Berkeley and  Daniel Elnatan, UCSF
# This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction.
# Disclaimer:  Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation. 
# 5 adj that describe spirit animal
# V1 2.9.21


import tkinter as tk
import vc2 as vc
import cv2
import numpy as np

###################### INITIALIZE GLOBAL VALUES #############################
vid=r'/users/anthonybravo/desktop/sfsu/csc667_opticalengineering/video/merced/0900m2_7.mp4';

xRez=1920; yRez=1080;
displayScale=1 # scale display output
window=[0,yRez,0,xRez]
winInc=10 # pixels
frameCount=0
Z=64
CROP=25
BUTTON_WIDTH=10  # button display width
WINDOW_SCALE=10   # window size increment
Z_SCALE=0.00001 # convert integer Z units to 10 um
FULL_SCALE=2   # reduce full scale image by this factor so it fits in window
xc=1082; yc=468;     # center of crop window
getCenter=False # flag that when sets xc,y, to mouse location on click
savePic=False # save pic of reconstruction when flag set

names = [
    ("Frame -10"),
    ("Frame -1"),
    ("Frame +1"),
    ("Frame +10"),
    ("Crop -10"),
    ("Crop -1"),
    ("Crop +1"),
    ("Crop +10"),
    ("Z -10"),
    ("Z -1"),
    ("Z +1"),
    ("Z +10"),
    ("SetBkg"), 
    ("ToggleBkg"),
    ("Display -1"),
    ("Display +1"), 
    (" "), 
    (" "),
    ("SavePic"),
    ("Center")
]

####################### PROCEDURES ##########################################
def doMouse(event,x,y,flags,param):
    global getCenter,xc,yc
    
    #print ("MOUSE EVENT",event,'getCenter',getCenter)
    if getCenter and event == cv2.EVENT_LBUTTONDOWN:
        xc,yc = x*FULL_SCALE,y*FULL_SCALE # compensate for full scale scaling
        # xc and yc must be even number for FFT to work
        if xc%2!=0:
            xc+=1
        if yc%2!=0:
            yc+=1
        #print ('updated center',xc,yc)
        processImage()
    return

def updateStatusDisplay():
    textOut='   Frame='+ str(frameCount) + '    Crop=' + str(CROP) + '    Z=' + str(Z) + '    Display=' + str(displayScale)+'   '
    tk.Label(root, text=textOut,bg="yellow",justify = tk.LEFT).grid(row=0,column=0,columnspan=4)
    return

def savePicture(holoIM,cropIM):
    global v 
    if 'mp4' in vid:
        name=vid[:-4]
    elif 'h264' in vid:
        name=vid[:-5]
    else:
        name=vid

    # save holo image
    imageName=name+'_'+str(frameCount)+'_'+str(xc)+'_'+str(yc)+'_'+str(Z)+'_holo.jpg'
    cv2.imwrite(imageName,holoIM)
    print ('Saved image',imageName)
    
    # save raw cropped image
    imageName=name+'_'+str(frameCount)+'_'+str(xc)+'_'+str(yc)+'_'+str(Z)+'_raw.jpg'
    cv2.imwrite(imageName,cropIM)

    v.set(2)  # set choice to "+1 Frame" so user won't be confused by SavePic being on
    return
    
def updateWindow():
    global window
    x0=xc-(WINDOW_SCALE*CROP)
    x1=xc+(WINDOW_SCALE*CROP)
    y0=yc-(WINDOW_SCALE*CROP)
    y1=yc+(WINDOW_SCALE*CROP)

    x0=clamp(x0,0,xRez)
    x1=clamp(x1,x0,xRez)
    y0=clamp(y0,0,yRez)
    y1=clamp(y1,y0,yRez)

    window=[y0,y1,x0,x1]
    print('Crop Window (um)',int(2*WINDOW_SCALE*CROP*1.4))
    return

def doButton():
    global frameCount,displayScale,Z,CROP,getCenter,savePic,bkgState,bkgIM

    getCenter=False #clear flag in case button is not Center, allows multiple centers until another button pushed
    val=v.get()
    but=names[val]

    increment=0
    if "-10" in but:
        increment=-10
    elif "+10" in but:
        increment=10
    elif "-1" in but:
        increment=-1
    elif "+1" in but:
        increment=1

    if 'Center' in but:
        getCenter=True  # this flag tells doCenter to update xc,yc
    elif 'SavePic' in but:
        savePic=True  # flag indicates picture capture requested
    elif 'Frame' in but:
        frameCount+=increment
        #frameCount=clamp(frameCount,0,MAX_FRAME-1)
    elif 'Z' in but:
        Z+=increment
        if Z<1:
            Z=1
    elif 'Display' in but:
        displayScale+=increment
        if displayScale<1:
            displayScale=1
    elif 'Crop' in but:
        CROP+=increment
        if CROP<1:
           CROP=1
    elif 'SetBkg' in but:
        #bkgIM=vc.getBkg(cap)
        pass
    elif 'ToggleBkg' in but:
        #bkgState+=1
        pass
    
    updateStatusDisplay()
    processImage()
    return


def processImage():
    global savePic
    
    updateWindow()
    (ret,rawIM)=vc.getFrame(cap,frameCount)
    grayIM = cv2.cvtColor(rawIM, cv2.COLOR_BGR2GRAY)
    if bkgState%2==1: # if odd enable background subtraction
        g2=grayIM/2
        b2=bkgIM/2
        grayIM=g2-b2

    cropIM=grayIM[window[0]:window[1],window[2]:window[3]] # crop window of image
    recoIM=vc.recoFrame(cropIM,Z*Z_SCALE)
    rescaleRecoIM=cv2.resize(recoIM,None,fx=displayScale,fy=displayScale)
    rescaleFullIM=cv2.resize(grayIM,None,fx=1.0/FULL_SCALE,fy=1.0/FULL_SCALE)

    cv2.imshow('Crop Reconstructed',rescaleRecoIM)
    cv2.imshow('Full Image',rescaleFullIM)
    cv2.waitKey(1)

    if savePic==True:
        savePicture(recoIM,cropIM) # save reconstructed and cropped raw image
        savePic=False   # reset flag so it ony does once per mouse click
    return

################################ MAIN ##################################
clamp = lambda value, minv, maxv: max(min(value, maxv), minv)

bkgState=0; # if odd, enable background subtraction
bkgIM=np.zeros((xRez,yRez),dtype='uint8') # background image

#cv2.namedWindow('Full Image')
root = tk.Tk()
v = tk.IntVar()
v.set(2)  # set choice to "+1 Frame"

root.title("Holographic Reconstruction")
updateStatusDisplay()

for val, txt in enumerate(names):
    r=int(1+val/4)
    c=int(val%4)
    tk.Radiobutton(root, text=txt,padx = 1, variable=v,width=BUTTON_WIDTH,command=doButton,indicatoron=0,value=val).grid(row=r,column=c)

cap=vc.openVid(vid)
processImage()
cv2.setMouseCallback('Full Image',doMouse)
MAX_FRAME=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print ("MAX_FRAME",MAX_FRAME)

root.mainloop()
cap.release()
cv2.destroyAllWindows()
print ('end program, bye')

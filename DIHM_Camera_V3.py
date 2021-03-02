'''
https://github.com/teph12/DIHM
Digital Inline Holographic Microscopy (DIHM)
Here we want to present an easy to use digital inline holographic microscope
employing 3D printed parts, a Raspberry Pi and Pi Cam, as well as a
high-power LED and a 15 micron pinhole. For details see (link to publication following).
https://www.nature.com/articles/s41598-019-47689-1

V3 2.18.21 Removed all the GPIO code, take one picture and close.
Name image with random number to prevent overright.
'''

import time
import picamera

path = "/home/pi/Desktop/holoImage/" 
with picamera.PiCamera() as camera:
    # set up camera
    #camera.resolution = (3280, 2464) # camera V2 (Sony IMX219, 1.12um pixel)   
    camera.resolution = (1592, 1944)  # camera V1 (OmniVision OV5647 1.4um pixel)  
    camera.iso = 100    #fixed iso
    camera.awb_mode = 'off'     
    camera.awb_gains = (1,3)    #fixed white balance

    # preview camaera
    camera.start_preview(resolution=(1440, 1080))
    time.sleep(2)

    # generate random number using timer
    r=str(int(time.time()*100))
    
    # capture and save image
    imageName='holo_'+r+'.jpg'
    camera.capture(path+imageName)
    

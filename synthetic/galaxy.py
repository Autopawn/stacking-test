import numpy as np
from random import randint,random

import skimage
import skimage.draw

def arm_points(revolutions=2.0,points=20):
    linsp = np.linspace(0,1,points)
    height = linsp
    expand = (1-linsp**4)/2.0
    center = 0.5+linsp*revolutions
    left_pts = np.array([center-expand,linsp]).T
    right_pts = np.array([center+expand,linsp]).T
    return np.concatenate((left_pts[:-1],right_pts[::-1]))

def add_random_galaxy(image,value=1,pos="RANDOM",rad1="RANDOM"):
    arms = randint(4,10)
    if rad1=="RANDOM":
        rad1 = (0.25+random()*0.25)*min(image.shape)
    if pos=="RANDOM":
        pos_y = image.shape[0]/2 + (random()-0.5)*(image.shape[0]-2*rad1)
        pos_x = image.shape[1]/2 + (random()-0.5)*(image.shape[1]-2*rad1)
        pos = (pos_y,pos_x)
    rad2 = (0.2+random()*0.8)*rad1
    rot = random()*2*np.pi
    phase = random()*2*np.pi
    rev = (2*randint(0,1)-1)*(1.0+random()*4.0)
    add_galaxy(image=image,value=value,arms=arms,pos=pos,rad1=rad1,rad2=rad2,
        rot=rot,rev=rev,phase=phase)

def add_galaxy(image,value=1,arms=6,pos=None,rad1=None,rad2=None,rot=0.0,
    rev=2.0,phase=0.0):
    # Calculate radious when they are not given
    if rad1 == None:
        rad1 = min(image.shape)*0.5
    if rad2 == None:
        rad2 = rad1
    if pos == None:
        pos = (image.shape[0]/2,image.shape[1]/2)
    # Get all the points in polar coords.
    arm_pts = arm_points(rev)
    points = []
    for i in range(arms):
        points.append((np.array(arm_pts)+[i,0])*[2*np.pi/arms,1]+[phase,0])
    points = np.concatenate(points)
    # Pass them to cartesian
    cpoints_x = np.cos(points[:,0])*points[:,1]*rad1
    cpoints_y = np.sin(points[:,0])*points[:,1]*rad2
    # Rotate and translate them
    rpoints_x = cpoints_x*np.cos(rot)-cpoints_y*np.sin(rot)+pos[0]
    rpoints_y = cpoints_x*np.sin(rot)+cpoints_y*np.cos(rot)+pos[1]
    # Draw them
    rr, cc = skimage.draw.polygon(rpoints_x,rpoints_y,image.shape)
    image[rr, cc] = value

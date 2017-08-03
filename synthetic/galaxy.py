import numpy as np

import skimage

ARM_POINTS = np.array([
    (0.0,0.5),(0.1,0.6),(0.2,0.75),(0.3,0.85),
    (0.4,0.9),(0.5,0.95),(0.7,1.0),(0.8,1.0),
    (0.9,1.0),(1.0,1.0),(1.1,1.0),(1.2,1.0),
    (1.25,0.9),(1.2,0.8),(1.1,0.75),(1.0,0.7),
    (0.9,0.65),(0.8,0.55),(0.75,0.5),(0.8,0.4),(0.9,0.4)])

def add_galaxy(image,value=1,arms=6,pos=None,rad1=None,rad2=None,rot=0):
    # Calculate radious when they are not given
    if rad1 == None:
        rad1 = min(image.shape)*0.5
    if rad2 == None:
        rad2 = rad1
    if pos == None:
        pos = (image.shape[0]/2,image.shape[1]/2)
    # Get all the points in polar coords.
    points = []
    for i in range(arms):
        points.append((np.array(ARM_POINTS)+[i,0])*[2*np.pi/arms,1])
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

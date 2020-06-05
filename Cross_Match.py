#########################################
#					#
# Cross Matching function		#
# Trystan Scott Lambert			#
#					#
# Function which mimics the astropy	#
# SkyCoord function but works for both	#
# cartesian, equitorial, and galacitc	#
#					#
# It is also much faster due to not	#
# assigning units to any arrays		#
# (except for some crash cases)		#
#					#
#########################################


import numpy as np 
import pylab as plt
import astropy.units as u 
from astropy.coordinates import SkyCoord

# Function to work out the xy cartesian distance. (only works for cartesian). 
def radii_distance(x1,x2,y1,y2):
	return np.sqrt((x1-x2)**2+(y1-y2)**2)

# Function to work out the distance between z1 and z2 (This works for both vel and/or z) 
def los_distance(z1,z2):
	return np.abs(z1-z2)

# In the case that we want to use the ra/dec/vel (or l,b,vel) we need calculate the angular separation. This is the explicit formulism
def angsep(ra1,ra2,dec1,dec2):
	try:
		faq=(np.pi/180)
		ra_1,ra_2,dec_1,dec_2=faq*ra1,faq*ra2,faq*dec1,faq*dec2
		cosl=np.cos((np.pi/2)-dec_2)*np.cos((np.pi/2)-dec_1)+np.sin((np.pi/2)-dec_2)*np.sin((np.pi/2)-dec_1)*np.cos(ra_2-ra_1)
		val=(1./faq)*np.arccos(cosl)
	except RuntimeWarning:
		c1=SkyCoord(ra=ra1*u.degree,dec=dec1*u.degree,frame='icrs')
		c2=SkyCoord(ra=ra2*u.degree,dec=dec2*u.degree,frame='icrs')
		sep=c1.separation(c2)
		val=sep.value
	return val

# Function which takes a point (x,y,z) and finds the closest point in x_array,y_array,z_array GIVEN some xy lim and then z lim. Weighted towards the xy lim. 
# This function will also work for RA/Dec/vel and l/b/vel (or any other distance metric)
# Note that xy-lim and z_lim are in cartesian coordinates or 3D Spherical depending out what the user puts in
def search_around_point(x,y,z,x_array,y_array,z_array,xy_lim,z_lim,frame='cartesian'):
	idx = np.arange(0,len(x_array))    #making an array representing the positions in the x_array
	
	if frame=='cartesian':						#checking which frame we are using. 
		os_distances = radii_distance(x,x_array,y,y_array) 	#if cartesian we get the distances in xy 
	elif frame=='spherical':
		os_distances = angsep(x,x_array,y,y_array)		#if spherical getting the distance in degrees
	
	os_cut = os_distances < xy_lim					#checking where the distances are less than the limit
	os_idx = idx[os_cut]						#applying our cut where distances are less than the limit

	los_distances = los_distance(z,z_array)				#working out all the line of sight distances 
	los_cut = los_distances < z_lim					#checking where the distances are less than the limit
	los_idx = idx[los_cut]						#applying our cut. 

	idx = np.intersect1d(los_idx,os_idx)				# This finds the common indicies between our 2 cuts. which means this shows the indicies in the arrays where both limits are passed  

	if len(idx)>1:							#in this case there are multiple matches to our one x,y,z point and we need to find the closest one
		print(f'{len(idx)} possible matches')			#printing out how many matches there are (We could remove this if need be)
		cut = np.where(os_distances[idx]==np.min(os_distances[idx]))[0] 	#This is finding the smallest distance 
		idx = idx[cut]						#This is getting the index in the array that is the closest match (which passes both limits)
		return idx[0],os_distances[idx][0],los_distances[idx][0]  
	
	elif len(idx) == 0:						# In this case there are no matches and so we can just return fokol
		print('No matches found')
		return None

	else:								# The only other possible thing is that there is exactly one match. 
		return idx[0],os_distances[idx][0],los_distances[idx][0]

#Function which will do the cross matching for an entire array
def Cross_match(x1,y1,z1,x2,y2,z2,xy_lim,z_lim,frame='cartesian'):
	# Error capturing to makes sure that the frame is correct. 
	if frame != 'cartesian' and frame != 'spherical':  
		print('Error: frame needs to be "cartesian" or "equitorial"')
		return  #returning nothing like this will end the function right away

	#lists which we will populate with values
	idx_1 = []	#this is the index for the x1,y1,z1 arrays
	idx_2 = []	#this is the corresponding index for x2,y2,z2
	d2d = []	#this is the on sky distances (either in cartesian units or degrees depending on frame choice)
	d3d = []	#this is the line-of-sight distance which will be in whatever units the user points in
	for i in range(len(x1)):
		val=search_around_point(x1[i],y1[i],z1[i],x2,y2,z2,xy_lim,z_lim,frame=frame) # returns the index in 2 with the closest match plus the offsets (on-sky and line-of-sight)
		if val != None:  #if val is empty (i.e. there isn't any match) then do nothing. I.e. only populate the lists if there is a match
			idx_1.append(i)
			idx_2.append(val[0])
			d2d.append(val[1])
			d3d.append(val[2])

	idx_1,idx_2,d2d,d3d = np.array(idx_1),np.array(idx_2),np.array(d2d),np.array(d3d) 
	
	idx_1_not_matches = np.setdiff1d(np.arange(0,len(x1)),idx_1)  #getting the inverses of the arrays so that we can find the failed matches. 
	idx_2_not_matches = np.setdiff1d(np.arange(0,len(x2)),idx_2)

	return idx_1,idx_2,idx_1_not_matches,idx_2_not_matches,d2d,d3d  #return them as arrays

# Cross_Matching
Function to Cross match astronomical catalogs in either cartesian, equitorial, or galactic coordinates with a preference on on-sky position

Cross matching between two catalogues is a tricky excercise due to the fact that one cannot garantee bijectivity, that is to say that sources from one catalog may or may not have several acceptable matches in another catalog. The inate ambigious nature causes a lot of difficulty in the Astronomy community. This is compounded when one has to consider multiple dimensions that can be searched around and the pseudo random search criteria that need to be chosen by the user. 

In order to circumnavigate some of these issues I present a cross matching function for specific use on astronomical catalogs and can cross match using either cartesian coordinates (xyz as one might find in HI data cubes), equitorial coordinates with some distance metric (such as velocity in extragalactic or physical distance), or galactic coordinates and a distance metric. 

There are multiple methods one might use to cross match catalogs. Here I present the method used by the Cross_match function. 

## Method

It is important from the onset that the user identify which catalog they wish to cross match to the other. Cross matching is not bijective and thus cross matching catalogA to catalogB is not necessarily the same as cross matching catalogB to catalogA and this is certainly not the case in this code. 

Astropy likes to use the markers c and catalog to differentiate between the users catalog and some "official" catalog. I will use the same notation but refrain the "catalog" connotation of being official. Both catalogs could, and often are, user based. 

starting from two catalogs we loop through the c catalog and for each value in c we perform a search in catalog for all values which fall within an xy limit (on-sky limit) and a line of sight limit (z_lim). The reasoning behind performing the cross match with two different axis (instead of a single axis as is done by astropy) is that often the onsky position of catalogs is much more accurate than the distance measurement. It is often if not always the case that one would prefer the line of sight limit to be larger than the on sky limit. 

Once all the cadidates in catalog which fall within the limits of c are identified the nearest ON SKY one is selected as the match to c. This is again because the on sky positions tend to be a lot more accurate. In the event that there is one match then this is taken as a match and if there are no matches then nothing is returned for that particular c value. 

The positon of the c value in c, the position of the catalog value in catalog are returned as well as the on sky separation between the two points (in cartesian or degrees depending on the user input) and the line of sight distance between the two points (in the units used by the user). 

This is done for the entire c array. At the end 6 arrays are returned namely 

idx1 = The posiitons of all the matches in the c arrays 
idx2 = The positions of all the matches in the catalog arrays 
idx1_nm = The positions of all the values in c which had no matches in catalog. 
idx2_nm = The positions of all the values in catalog which weren't found as matches 
d2d = The onsky difference for all the matches 
d3d = The line of sight offset between all the matches

### Cartesian Example
The below will cross match c = (x_c,y_c,z_c) to catalog = (x_cat,y_cat,z_cat) with a 20 pixel on-sky limit and a 200 pixel line of sight limit

import Cross_Match as cm

xy_lim = 20

z_lim = 200

idx_c,idx_cat,idx_not_matches_c,idx_not_matches_cat,d2d,d3d = cm.Cross_match(x_c,y_c,z_c,x_cat,y_cat,z_cat,xy_lim,z_lim)

### Equitorial Example
The code below will cross mathc c = (ra_c,dec_c,vel_c) to catalog = (ra_cat,dec_cat,vel_cat) with a 2 degree onsky limit and a 200 km/s line of sight limit

import Cross_Match as cm 

on_sky_lim = 2

los_lim = 200

idx_c,idx_cat,idx_not_matches_c,idx_not_matches_cat,d2d,d3d = cm.Cross_match(ra_c,dec_c,vel_c,
                                            ra_cat,dec_cat,vel_cat,on_sky_lim,los_lim,frame='Spherical')


### Galactic Example
The code below will cross match c = (l_c,b_c,dist_c) to catalog = (l_cat,b_cat,dist_cat) with a 30 arcsecond onsky limit and a 10 Mpc line of sight limit 

import Cross_Match as cm 

on_sky_lim = 30/3600 # Have to convert into decimal degrees

los_lim = 4

idx_c,idx_cat,idx_not_matches_c,idx_not_matches_cat,d2d,d3d = cm.Cross_match(l_c,b_c,dist_c,
                                            l_cat,b_cat,dist_cat,on_sky_lim,los_lim,frame='Spherical')

## Installation

Download the repository through Git.

`git clone https://github.com/TrystanScottLambert/Cross_Matching.git`

## Execution
This script can be downloaded and read in as one would a python package i.e. import Cross_Match as cm. From there the limited number of functions can be used

The main function is Cross_match and is the one which should be used most often. This takes 2 sets of positional arrays and cross matches the first one into the other returning a list of indicies matches in the 1st, indicies matches in the 2nd, indicies which couldn't find a match in the 1st, indicies which couldn't find a match in the 2nd, the on sky separation between the matches and the line of sight offesets between the matches. 
`

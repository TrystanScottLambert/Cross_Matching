# Cross_Matching
Function to Cross match astronomical catalogs in either cartesian, equitorial, or galactic coordinates with a preference for on-sky position.

Cross matching between two catalogues is a tricky excercise due to the fact that one cannot guarantee bijectivity; that is to say that sources from one catalog may or may not have several acceptable matches in another catalog. The inate ambigious nature causes a lot of difficulty in the astronomy community. This is compounded when one has to consider multiple dimensions that can be searched around and the pseudo-random search criteria that need to be chosen by the user. 

In order to circumnavigate some of these issues I present a cross matching function for specific use on astronomical catalogs. It can cross match using either cartesian coordinates (xyz as one might find in HI data cubes), equitorial coordinates with some distance metric (such as velocity in extragalactic or physical distance), or galactic coordinates and a distance metric. 

There are multiple methods one might use to cross match catalogs. Here I present the method used by the Cross_match function. 

## Method

It is important from the onset that the user identifies which catalog they wish to cross match to the other. Cross matching is not bijective and thus cross matching catalogA to catalogB is not necessarily the same as cross matching catalogB to catalogA and this is certainly not the case in this code. 

Astropy likes to use the markers c and catalog to differentiate between the two catalogs. I will use the same notation.

Starting from two catalogs, we loop through the "c" catalog and for each value in "c" we perform a search in "catalog" for all values which fall within an xy limit (on-sky limit) and a line-of-sight limit (z limit). The reasoning behind performing the cross match with two different axis (instead of a single axis as is done by astropy) is that often the on-sky position of astronomical catalogs are much more accurate than the distance measurement. It is almost always the case that one would prefer the line-of-sight limit to be larger than the on-sky limit. 

Once all the candidates in "catalog" which fall within the limits of "c" are identified, the nearest ON-SKY match in "catalog" is selected as the match to the "c" entry. This is, again, because the on-sky positions tend to be a lot more accurate. In the event that there is one match then this is taken as a match and if there are no matches then nothing is returned for that particular "c" entry. 

What is returned:
- The positon of the c value in "c" 
- the position of the catalog value in "catalog"
- the on-sky separation between the two points (in cartesian coords or degrees, depending on the user input)
- the line-of-sight distance between the two points (in the units used by the user, e,g, km/s, Mpc, GHz). 

This is done for the entire "c" array. At the end, 6 arrays are returned, namely:

idx1 = The positions of all the matches in the "c" arrays
idx2 = The positions of all the matches in the "catalog" arrays
idx1_nm = The positions of all the values in "c" which had no matches in "catalog". 
idx2_nm = The positions of all the values in "catalog" which weren't found as matches 
d2d = The on-sky difference for all the matches
d3d = The line-of-sight offset between all the matches

### Cartesian Example
The code below will cross match c = (x_c,y_c,z_c) to catalog = (x_cat,y_cat,z_cat) with a 20 pixel on-sky limit and a 200 pixel line-of-sight limit

```

import Cross_Matching.Cross_Match as cm

xy_lim = 20
z_lim = 200

idx_c,idx_cat,idx_not_matches_c,idx_not_matches_cat,d2d,d3d = cm.Cross_match(x_c,y_c,z_c,x_cat,y_cat,z_cat,xy_lim,z_lim)

```

### Equitorial Example
The code below will cross match c = (ra_c,dec_c,vel_c) to catalog = (ra_cat,dec_cat,vel_cat) with a 2 degree on-sky limit and a 200 km/s line-of-sight limit

```
import Cross_Matching.Cross_Match as cm 

on_sky_lim = 2
los_lim = 200

idx_c,idx_cat,idx_not_matches_c,idx_not_matches_cat,d2d,d3d = cm.Cross_match(ra_c,dec_c,vel_c,ra_cat,dec_cat,vel_cat,on_sky_lim,los_lim,frame='spherical')

```

### Galactic Example
The code below will cross match c = (l_c,b_c,dist_c) to catalog = (l_cat,b_cat,dist_cat) with a 30 arcsecond on-sky limit and a 10 Mpc line-of-sight limit 

```
import Cross_Matching.Cross_Match as cm 

on_sky_lim = 30/3600 # Have to convert into decimal degrees
los_lim = 10

idx_c,idx_cat,idx_not_matches_c,idx_not_matches_cat,d2d,d3d = cm.Cross_match(l_c,b_c,dist_c,l_cat,b_cat,dist_cat,on_sky_lim,los_lim,frame='spherical')

```

## Installation

#### Git Clone Method 
Download the repository through Git.

`git clone https://github.com/TrystanScottLambert/Cross_Matching.git`

This script can be downloaded and read in as one would a python package i.e. import Cross_Match as cm. Make sure that the Cross_Match.py script is in the same folder as the script you want to use. You may use this script in any fashion as you see fit.

#### pip install method

Alternatively one could simply pip install the package using the python 3 version of pip

` pip install Cross_Matching `

It can then be run in scripts 

` import Cross_Matching.Cross_Match as cm `

## Execution

The main function is Cross_match and is the one which should be used most often. This takes 2 sets of positional arrays and cross matches the first one into the other, returning a list of indicies matches in the 1st, indicies matches in the 2nd, indicies which couldn't find a match in the 1st, indicies which couldn't find a match in the 2nd, the on-sky offsets between the matches and the line-of-sight offsets between the matches. 


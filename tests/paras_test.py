# -*- coding: utf-8 -*-
"""
Parameter file for the a single simulation. The Paras object in output should
be always processed by post_process_paras in utilities file.
"""

from os.path import join as jn
import pickle as _pickle
import sys as _sys
from math import ceil as _ceil
	
from abm_strategic.utilities import Paras as _Paras

from abm_strategic import main_dir

version = '2.9.5' # Forked from version 2.9.5 of ABMvars.

##################################################################################
################################### Parameters ###################################
##################################################################################

# Unit of time
unit = 20. # used to translate times (from instance tau) in minutes.

# ---------------- Network Setup --------------- #
# Use None if you want to generate a new network (based on paras_G file).

file_net = jn(main_dir, 'tests', 'network_test.pic')
capacity_factor = 1. # expand all capacities by this factor.

# ---------------- Companies ---------------- #

Nfp = 10 								# Number of flight plans to submit for a flight (pair of departing-arriving airports)
Nsp_nav = 10 							# Number of shortest paths of navpoints per path of sector.
na = 1  								# Number of flights (pairs of departing-arriving airports) per company. Never tested for na>1.
tau = 1.*unit							# Increment of time for shifting flight plans.

# ------- Density and times of departure patterns ------- #

day=24.*60. 							# Total duration of the simulation in minutes.

# One can specify a file to extract flows (i.e. departure times, entry exit, densities, etc.)
# Leave None for new generation of traffic. 
# You can specify ACtot even if you give a file, in which case the code will extract the distribution of 
# flows (entry/exit + times of departure)

file_traffic = None     
if file_traffic==None:
	# These variables are not fully independent and might be overwritten depending on
	# the type of control you choose.
	ACtot = 100 						# Relevant for choosing the total number of ACss.
	density = 20          				# Relevant for choosing an overall density of flights
	control_density = False				# If you want to set the density rather than the number of flights.
	
	departure_times = 'square_waves' #departing time for each flight, for each AC

	#One can also specifiy a file only for times of departures.
	file_times = None
	if file_times==None:
		if departure_times=='square_waves':
			width_peak = unit 			# Duration of a wave
			Delta_t = unit*1      		# Time between the end of a wave and the beginning of the next one.
			ACsperwave = 30				# Relevant for choosing a number of ACs per wave rather than a total number
			control_ACsperwave = True	# True if you want to control ACsperwave instead of density/ACtot

	starting_date = [2010, 5, 6, 0, 0, 0] # This is just used to create artificial dates.
else:
	bootstrap_mode = False	# if False, times of departures and entry/exits are exactly matched 
							# the data. Otherwise, they are generated from the distribution extracted 
							# on the data.
	if bootstrap_mode:
		bootstrap_only_time = True 	# if True, keeps the same number of flights (scaled down or scaled down if ACtot is specified)
									# for each entry/exit but extract new desired times from all times 
		ACtot = 1000 # if commented, will be matched to the number of flights in the traffic file
		
noise = 0. 								# noise on departures in minutes.

# ------------------ Behavioral parameters ---------------- #
nA = 1.                        			# percentage of Flights of the first population.
par = [[1.,0.,0.001], [1.,0.,1000.]]		# Parameters of the utility function for each population.

# ------------------- From M0 to M1 ----------------------- #
mode_M1 = 'standard' # sweep or standard
if mode_M1 == 'standard':
	# In this mode, the N_shocks network are shut down. 
	N_shocks = 0  						# Total number of sectors to shut
else: 
	# In this mode, only one sector is shut down (used principally for iterations over shocks)
	STS = None  #Sectors to Shut
	

# --------------------System parameters -------------------- #
parallel = False						# Parallel computation or not
old_style_allocation = False			# Don't remember what this is. Computation of load?
force = True							# force overwrite of already existing simulation (based on name of file).


##############################################################

# ---------------- Building paras dictionary --------------- #
# Do not modify.
paras = _Paras({k:v for k,v in vars().items() if k[:1]!='_' and k!='version' and k!='Paras' and not k in [key for key in locals().keys()
           if isinstance(locals()[key], type(_sys)) and not key.startswith('__')]})
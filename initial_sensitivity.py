import numpy as np
from loads_dictionary_function import loads_dict
from load_and_analyze import Inp2Analysis

inp_filename = 'standard_channel_L10_0.inp'
inputs = np.load('saltelli_inputs.npy')

#r_disps = [0., 1., 2.]
#s_disps = [0., 0.05, 0.1]
#t_disps = [0., 0.01, 0.02]
#l_disps = [-0.03, -0.015, 0., 0.015, 0.03]
#
#for r in r_disps:
#    for s in s_disps:
#	for t in t_disps:
#	    for l in l_disps:
#		if r == 0 and s == 0 and t == 0 and l == 0:
#		    continue
#		else:
#		    loads = loads_dict(r_loads=[r], s_loads=[s],
#			    t_loads=[t], l_loads=[l])
#

for load in loads:
    print >> sys.__stdout__, load

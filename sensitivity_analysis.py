from load_and_analyze import *
from loads_dictionary_function import loads_dict
from get_stresses import *

r_disps = [0., 1., 2.]
s_disps = [0., 0.05, 0.1]
t_disps = [0., 0.01, 0.02]
l_disps = [-0.03, -0.015, 0., 0.015, 0.03]

for r in r_disps:
    for s in s_disps:
	for t in t_disps:
	    for l in l_disps:
		if r == 0 and s == 0 and t == 0 and l == 0:
		    continue
		else:
		    loads = loads_dict(r_loads=[r], s_loads=[s],
			    t_loads=[t], l_loads=[l])

inp_filename = 'standard_channel_L10_0.inp'

#for load in loads:
#    analysis = Inp2Analysis(inp_filename)
#    analysis.import_inp()
#    bcs = loads[load]
#    analysis.define_bcs(bcs)
#    analysis.run_analysis(load, numCpus=40)
#
coords = np.array([np.linspace(0, 0, 20), np.linspace(-2.8, 0.9, 20), np.linspace(0.2, 12.5, 20)])

load_arr = np.empty((0, 1))
stress_arr = np.empty((0,1))
dir_arr = np.empty((0,3))
loc_arr = np.empty((0,3))

for load in loads:

    analysis = Inp2Analysis(inp_filename)
    analysis.import_inp()
    analysis.define_bcs(loads[load])
    analysis.run_analysis(load)

    odb_filename = load+'.odb'
    max_principal, direction, loc = get_max_principal_stress_and_direction(odb_filename, coords)
    load_arr = np.append(load_arr, np.array([[load]]), axis=0)
    stress_arr = np.append(stress_arr, np.array([[max_principal]]), axis=0)
    dir_arr = np.append(dir_arr, np.array([direction]), axis=0)
    loc_arr = np.append(loc_arr, np.array([loc]), axis=0)

    np.save('load_name', load_arr)
    np.save('max_principal', stress_arr)
    np.save('locations', loc_arr)
    np.save('directions', dir_arr)

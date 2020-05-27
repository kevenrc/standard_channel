import numpy as np
import pandas as pd
import sys
import os
import glob
from emery_driver import *

##############
#parameters for the crack_growth function to work properly
original_mesh_file = 'standard_channel_L10_4.inp'
retained_elems_filename = 'RETAINED_ELEMS_chamfer.txt'
init_crack_size = 0.05
previous_step = 2
steps = 8
median_step_size = 0.24
template_radius = 0.01
poly_order = 3
ex_A, ex_B = 8, 8
smoothing_method = "CUBIC_SPLINE"
discard_ = 2
exe = 'abaqus'
num_processors = 16
#############

df = pd.read_csv('uncracked_results.csv')

for odb_filename in glob.glob('*.odb'):

#    odb_filename = load+'.odb'
    base_odb_filename = os.path.basename(odb_filename)
    root_name = base_odb_filename.replace('.odb', '')
    root_filename = odb_filename.replace('.odb', '').replace('odb_files', 'inp_files')

    results = df[df['root_name'] == root_name]

    crack_location = list(np.round(results[['loc_x', 'loc_y', 'loc_z']], 1).to_numpy().flatten())
    direction = list(results[['dir_x', 'dir_y', 'dir_z']].to_numpy().flatten())

    phi = np.arccos(direction[2])*180/np.pi
    theta = np.arctan(direction[1]/direction[0])*180/np.pi
    rotation = [int(phi), int(theta)]
    print(crack_location)
    print(rotation)

    insert_and_grow_crack(root_name, retained_elems_filename, init_crack_size,
	    crack_location, rotation, previous_step, steps, median_step_size, template_radius,
	    poly_order, ex_A, ex_B, smoothing_method, discard_, exe, num_processors, initial_crack=False)

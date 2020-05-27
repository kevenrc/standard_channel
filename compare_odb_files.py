import glob
import numpy as np
from load_and_analyze import OdbPointsResults

#loads = ['r-load', 's-load', 't-load', 'l-load-pos', 'l-load-neg']
loads = ['s-load']
#npy_files = ['rload', 'sload', 'tload', 'lload', '-lload']
npy_files = ['sload']
points = np.load('standard_channel_rload_presto.e.npy')

for load, npy_file in zip(loads, npy_files):
    odb_path = os.path.join(load+'.odb')
    odb_results = OdbPointsResults(points)
    odb_results.open_odb(odb_path)
    odb_results.define_path()
    odb_results.get_displacements()

#    odb_path_nl = os.path.join(load+'-nl', load+'-nl.odb')
#    odb_results_nl = OdbPointsResults(points)
#    odb_results_nl.open_odb(odb_path_nl)
#    odb_results_nl.define_path()
#    odb_results_nl.get_displacements()

    struct_disp = np.load('standard_channel_'+npy_file+'_presto.e.npy')
    diff_u1 = odb_results.u1 - struct_disp[3]
    diff_u2 = odb_results.u2 - struct_disp[4]
    diff_u3 = odb_results.u3 - struct_disp[5]
    diff_array = np.array([diff_u1, diff_u2, diff_u3])
    disp_3d = np.array([odb_results.u1, odb_results.u2, odb_results.u3])
    np.save(load+'_3d.npy', disp_3d)
    np.save(load+'_diff.npy', diff_array)


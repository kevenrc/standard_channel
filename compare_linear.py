from load_and_analyze import OdbPointsResults
import numpy as np

s_loads = np.linspace(0.1015, 0.5075, num=5)
t_loads = np.linspace(0.0254, 0.127, num=5)

def compare_and_save(coords, load, disp):
    odb_path = load+'/'+load+str(disp).replace('.','')+'.odb'
    odb_path_nl = load+'-nl/'+load+'-nl'+str(disp).replace('.','')+'.odb'
    odb_results = OdbPointsResults(coords)
    odb_results.open_odb(odb_path)
    odb_results.define_path()
    odb_results.get_displacements()
    odb_results_nl = OdbPointsResults(coords)
    odb_results_nl.open_odb(odb_path_nl)
    odb_results_nl.define_path()
    odb_results_nl.get_displacements()

    diff_u1 = odb_results.u1 - odb_results_nl.u1
    diff_u2 = odb_results.u2 - odb_results_nl.u2
    diff_u3 = odb_results.u3 - odb_results_nl.u3
    diff_array = np.array([diff_u1, diff_u2, diff_u3])

    np.save(load+str(disp).replace('.','')+'_nl_diff', diff_array)

coords = np.load('npy_files/standard_channel_rload_presto.e.npy')

#for disp in s_loads:
#    compare_and_save(coords, 's-loads', disp)
#
for disp in t_loads:
    compare_and_save(coords, 't-loads', disp)


import PyF3D

f3d = PyF3D.F3DApp()

# FRANC3D Version 7.3


f3d.OpenFdbModel(
    file_name='l-load-pos_LOCAL_crack_STEP_005.fdb',
    orig_mesh_file='l-load-pos_LOCAL.inp',
    global_file='l-load-pos_GLOBAL.inp',
    mesh_file='l-load-pos_LOCAL_crack_STEP_005.inp',
    resp_file='l-load-pos_LOCAL_crack_STEP_005_full.dtp')

f3d.WriteSifPath(
    file_name='sif_history.sif',
    load_step=1,
    final_step=5,
    flags=["TAB","A","KI","KII","KIII","CRD"])


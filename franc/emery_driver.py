import PyF3D
import os
import numpy as np

f3d = PyF3D.F3DApp()

# file names
root_name = 'l003'   # 000.fdb'
retained_elems_filename = 'RETAINED_ELEMS_chamfer.txt'
#orig_mesh_file='fatigue_case1BCs_LOCAL.i'
#global_file='fatigue_case1BCs_GLOBAL.i'
#mesh_file='50micron_45degree_BCs1_IplusII_'   # 000.i'
#resp_file='50micron_45degree_BCs1_IplusII_'   # 000_full.e'
# number of crack growth steps
steps = 13

#crack growth parameters
# : steps 000
previous_step = 1
median_step_size = 0.17
init_crack_size = 0.05
template_radius = 0.01
poly_order=3
discard_=2
ex_A,ex_B = 14, 14
location = [0., -2.75, 6.45]
rotation = [89, 67]
smoothing_method = "CUBIC_SPLINE"
# analysis variables
num_processors = 16
exe='abaqus'

##
##
####### shouldn't need to modify below this

## helper functions
def split_local_global(root_name, retained_elems_filename):
    f3d.Submodeler(
        model_type="ABAQUS",
        orig_file_name=root_name+'.inp',
        submodel_file_name=root_name+'_LOCAL.inp',
        global_file_name=root_name+'_GLOBAL.inp',
        elem_file_name=retained_elems_filename)
    return root_name+'_GLOBAL.inp', root_name+'_LOCAL.inp'

def analysis_b4_growth(root_name, init_crack_size, location, rotation, exe='abaqus', num_processors=16):
    f3d.OpenMeshModel(
        model_type="ABAQUS",
        file_name=root_name+'_LOCAL.inp',
        global_name=root_name+'_GLOBAL.inp')
    
    f3d.InsertParamFlaw(
        flaw_type="CRACK",
        crack_type="EMESH",
        flaw_params=[init_crack_size, init_crack_size],
        rotation_axes=[2, 3],
        rotation_mag=rotation,
        translation=location,
        radius=init_crack_size/9)

    f3d.RunAnalysis(
	model_type="ABAQUS",
	file_name='{}_crack_STEP_000.fdb'.format(root_name),
	flags=["NO_WRITE_TEMP","TRANSFER_BC","NO_CFACE_TRACT","NO_CFACE_CNTCT"],
	merge_tol=0.0001,
	connection_type="MERGE",
	executable=exe,
	command='{} job={}_crack_STEP_000_full cpus={} -interactive -analysis'.format(exe, root_name, num_processors),
	global_model=root_name+'_GLOBAL.inp')

    f3d.ComputeSif()

    f3d.SetUnits(
        model_length="UNKNOWN",
        model_stress="UNKNOWN",
        temperature="UNKNOWN")

    f3d.SetGrowthParams(
        growth_type="QUASI_STATIC",
	load_step_map=["VERSION: 1","MAX_SUB: 1","-1 0","LABELS: 1","1 Load Step 1"],
        kink_angle_strategy="MTS",
        quasi_static_n=2,
        quasi_static_loads=["ONE_STEP: 1 NONE 1 1 0"],
        median_step=median_step_size/2,
	cycles_step=1000,
        front_mult=[1])

    f3d.GrowCrack(
	median_step=0.17,
	cycles_step=1000,
	front_mult=[1],
	temp_radius_type="ABSOLUTE",
	temp_radius=0.014,
	smoothing_method=["FIXED_ORDER_POLY"],
	polynomial_order=[poly_order],
	discard=[[2,2]],
	extrapolate=[[8,8]])

    f3d.RunAnalysis(
	model_type="ABAQUS",
	file_name='{}_crack_STEP_001.fdb'.format(root_name),
	flags=["NO_WRITE_TEMP","TRANSFER_BC","NO_CFACE_TRACT","NO_CFACE_CNTCT"],
	merge_tol=0.0001,
	connection_type="MERGE",
	executable=exe,
	command='{} job={}_crack_STEP_001_full cpus={} -interactive -analysis'.format(exe, root_name, num_processors),
	global_model=root_name+'_GLOBAL.inp')

def openModel(fname, orig_mesh_file, global_file):
    f3d.OpenFdbModel(
        file_name='{}.fdb'.format(fname),
        orig_mesh_file=orig_mesh_file, global_file=global_file,
        mesh_file='{}.inp'.format(fname),
        resp_file='{}_full.dtp'.format(fname))

def initiateModel():
    f3d.ComputeSif()

    f3d.SetUnits(
        model_length="UNKNOWN",
        model_stress="UNKNOWN",
        temperature="UNKNOWN")

    f3d.SetGrowthParams(
        growth_type="QUASI_STATIC",
        load_step_map=["VERSION: 1","MAX_SUB: 1","-1 0","LABELS: 1","1 Load Step 1"],
        kink_angle_strategy="MTS",
        quasi_static_n=2,
        quasi_static_loads=["ONE_STEP: 1 NONE 1 1 0"],
        median_step=median_step_size,
        cycles_step=1000,
        front_mult=[1])

    ###
def insert_and_grow_crack(root_name, retained_elems_filename, init_crack_size,
	location, rotation, previous_step, steps, median_step_size, template_radius,
	poly_order, ex_A, ex_B, smoothing_method, discard_, exe, num_processors, initial_crack=True):

    global_file, orig_mesh_file = split_local_global(root_name, retained_elems_filename)
    if initial_crack:
	analysis_b4_growth(root_name, init_crack_size, location, rotation)
    fname = root_name + '_crack_STEP_{:03}'.format(previous_step)
    print fname
    openModel(fname, orig_mesh_file, global_file)
    print fname

    for i in range(previous_step+1,previous_step+steps+1):

	fname = root_name + '_crack_STEP_{:03}'.format(i)
	print fname

	initiateModel()

	temp_step = median_step_size
	tempInc = template_radius
	temp_poly_order = poly_order 
	temp_ex_A = ex_A
	temp_ex_B = ex_B
	temp_smoothing_method = smoothing_method
	while 1:
	    try:
		f3d.GrowCrack(
		    median_step=temp_step,
		    cycles_step=1000,
		    temp_radius_type="ABSOLUTE",
		    temp_radius=tempInc,
		    smoothing_method=[smoothing_method],
		    polynomial_order=[temp_poly_order],
		    discard=[[discard_,discard_]],
		    extrapolate=[[temp_ex_A,temp_ex_B]])
		print ' *** Crack growth successful for {} *** '.format(fname)
		break
	    except RuntimeError:
		tempInc = tempInc * (1 + 0.1*( np.random.random())) # nudge increment updward
		temp_step = temp_step * (1 + 0.1*(np.random.random()))
		print "RuntimeError caught. \n  Randomly adjusting template radius to {:1.3f}".format(tempInc)
		print "Randomly adjusting crack growth step to {:1.3f}".format(temp_step)
		temp_poly_order = int(np.random.choice([1, 2, 3, 4, 5]))
		temp_smoothing_method = str(np.random.choice(["CUBIC_SPLINE", "MOVING_POLY", "FIXED_ORDER_POLY"]))
		print "changing poly order to {}".format(temp_poly_order)
		print "changing smoothing method to {}".format(temp_smoothing_method)
		# Close and reopen f3d model
		f3d.CloseModel()
		lastFName =  root_name + '_crack_STEP_{:03}'.format(i-1)
		openModel(lastFName)
		initiateModel()
		continue
	    else:
		print ' ** Crack growth unsuccessful for {} ** '.format(fname)
		break


	f3d.RunAnalysis(
	    model_type="ABAQUS",
	    file_name='{}_crack_STEP_{:03}.fdb'.format(root_name,i),
	    flags=["NO_WRITE_TEMP","TRANSFER_BC","NO_CFACE_TRACT","NO_CFACE_CNTCT"],
	    merge_tol=0.0001,
	    connection_type="MERGE",
	    executable=exe,
	    command='{} job={}_crack_STEP_{:03}_full cpus={} -interactive -analysis'.format(exe, root_name, i, num_processors),
	    global_model=global_file)

	#os.system('rm *STEP_{:03}_full*'.format(i-1)) # delete the previous files

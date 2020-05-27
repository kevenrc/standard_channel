import sys
import glob
import numpy as np

from load_and_analyze import OdbPointsResults as opr

def get_max_principal_stress_and_direction(odb_filename, coords):

    odb = opr(coords)
    odb.open_odb(odb_filename)
    odb.define_path()
    odb.get_stresses()

    max_principal = max(odb.max_principal)
    loc = odb.coord_nums[np.argmax(odb.max_principal)] - 1
    loc33 = np.argmax(odb.max_principal)

    a = (odb.S22[loc] - max_principal)*(odb.S33[loc33] - max_principal) - odb.S23[loc]**2
    b = -(odb.S12[loc]*(odb.S33[loc33] - max_principal) - odb.S13[loc]*odb.S23[loc])
    c = odb.S12[loc]*odb.S23[loc] - odb.S13[loc]*(odb.S22[loc] - max_principal)

    k = 1 / np.sqrt(a**2 + b**2 + c**2)

    l = a*k
    m = b*k
    n = c*k

    return max_principal, np.array([l, m, n]), coords[:, loc]

def parse_filename(odb_filename):

    direction = odb_filename[0]
    end = odb_filename.find('.')
    start = 15
    displacement = odb_filename[start:end]
    displacement = displacement[:1] + '.' + displacement[1:]

    return direction, float(displacement)

if __name__ == "__main__":

    coords = np.array([np.linspace(0, 0, 20), np.linspace(-3., 1.5, 20), np.linspace(0., 12.7, 20)])

    odb_files = glob.glob('*/*.odb')
    load_arr = np.empty((0,1))
    disp_arr = np.empty((0,1))
    stress_arr = np.empty((0,1))

    for odb_filename in odb_files:

        print >> sys.__stdout__, odb_filename

	max_principal, direction, loc = get_max_principal_stress_and_direction(odb_filename, coords)
	load_direction, load_disp = parse_filename(odb_filename)
	load_arr = np.append(load_arr, np.array([[load_direction]]), axis=0)
	disp_arr = np.append(disp_arr, np.array([[load_disp]]), axis=0)
	stress_arr = np.append(stress_arr, np.array([[max_principal]]), axis=0)

        print >> sys.__stdout__, load_disp
        print >> sys.__stdout__, max_principal
	np.save('load_direction', load_arr)
	np.save('load_displacement', disp_arr)
	np.save('max_principal', stress_arr)


import numpy as np
import glob

for filename in glob.glob("*diff.npy"):
    array = np.load(filename)
    np.savetxt(filename.replace('.npy', '.csv'), array, delimiter=',')

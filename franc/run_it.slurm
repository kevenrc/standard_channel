#!/bin/bash
#SBATCH --time=72:00:00 # walltime, abbreviated by -t
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=kevenrc@gmail.com
#SBATCH --nodes=1
#SBATCH --ntasks=40
# additional information for allocated clusters
#SBATCH --account=hochhalter-gpu-np     # account - abbreviated by -A
#SBATCH --partition=hochhalter-gpu-np # partition, abbreviated by -p

#
# set data and working directories
export WORKDIR=/uufs/chpc.utah.edu/common/home/u0823391/Desktop/standard_channel/franc
export SCDIR=/scratch/kingspeak/serial/u0823391/franc/$SLURM_JOBID

export PYTHONPATH=$PYTHONPATH:/uufs/chpc.utah.edu/common/home/u0823391/Desktop/standard_channel/
mkdir -p $SCDIR
cp -r * $SCDIR
cd $SCDIR
cp ../inp_files/r0015s001t002l0015.inp ../odb_files/r0015s001t002l0015.odb ./
echo Working in $SCDIR
# load appropriate modules, in this case Intel compilers, MPICH2
module load abaqus/2019
module load anaconda3
source /uufs/chpc.utah.edu/sys/installdir/anaconda3/5.1.0/bin/activate py2

unset SLURM_GTIDS

python crack_growth.py
#abaqus cae noGUI=prelim_crack_growth.py

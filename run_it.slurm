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
export WORKDIR=/uufs/chpc.utah.edu/common/home/u0823391/Desktop/standard_channel/
export SCDIR=/scratch/kingspeak/serial/u0823391/abaqus/$SLURM_JOBID

mkdir -p $SCDIR
cp * $SCDIR
cd $SCDIR
echo Working in $SCDIR
# load appropriate modules, in this case Intel compilers, MPICH2
module load abaqus/2019

unset SLURM_GTIDS

abaqus cae noGUI=sensitivity_analysis.py

#!/usr/bin/bash
#
#SBATCH --job-name=mrlavaloba
#SBATCH --output=out_%j.txt
#SBATCH --ntasks=1
#SBATCH --time=45:00
#######SBATCH -w, ru-cn-1

echo "Running mrlavaloba on a single CPU core"

/scratch/hpc_2022/fjolnir/MrLavaLoba/run_lava

date

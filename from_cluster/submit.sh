#!/usr/bin/bash
#
#SBATCH --job-name=mrlavaloba
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=melissa@vedur.is     # Where to send mail
#SBATCH --output=out_%j.txt
#SBATCH --ntasks=1
#SBATCH --time=45:00
#######SBATCH -w, ru-cn-1

echo "Running mrlavaloba on a single CPU core"

/scratch/hpc_2022/fjolnir/MrLavaLoba/run_lava

date

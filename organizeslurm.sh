#!/usr/bin/bash
#SBATCH --job-name=organize
#SBATCH --time=02:00:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

# OBS_DATE=2026-03-10 (Si no pones el dia usa el de ayer)
source /fefs/aswg/workspace/manuel.martinezherresanchez/limpieza/lst-utils/osa-env.sh



/usr/bin/bash /fefs/aswg/workspace/manuel.martinezherresanchez/limpieza/lst-utils/launch_organize.sh -s --no-gainsel --no-running

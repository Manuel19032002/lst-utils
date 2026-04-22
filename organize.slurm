#!/usr/bin/bash
#SBATCH --job-name=organize
#SBATCH --time=02:00:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

source /fefs/aswg/workspace/manuel.martinezherresanchez/limpieza/lst-utils/osa-env.sh



/usr/bin/bash /fefs/aswg/workspace/manuel.martinezherresanchez/limpieza/lst-utils/launch_organize.sh -s --no-gainsel --no-running

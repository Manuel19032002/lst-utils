#!/bin/env python

#SBATCH --job-name=LST1_20994
#SBATCH --time=2:00:00
#SBATCH --chdir=/fefs/onsite/data/lst-pipe/LSTN-01/running_analysis/20250702/v0.11
#SBATCH --output=log/Run20994.%4a_jobid_%A.out
#SBATCH --error=log/Run20994.%4a_jobid_%A.err
#SBATCH --partition=short,long
#SBATCH --mem-per-cpu=6GB
#SBATCH --account=osa

import os
import subprocess
import sys
import tempfile

os.environ['CTAPIPE_CACHE'] = '/fefs/aswg/data/ctapipe_service'
os.environ['CTAPIPE_SVC_PATH'] = '/fefs/aswg/data/ctapipe_service'
os.environ['MPLCONFIGDIR'] = '/fefs/aswg/data/aux/matplotlib'
subruns = os.getenv('SLURM_ARRAY_TASK_ID')

with tempfile.TemporaryDirectory() as tmpdirname:
    os.environ['NUMBA_CACHE_DIR'] = tmpdirname
    proc = subprocess.run([
        'conda',
        'run',
        '-n',
        'lstcam-env',
        'calibration_pipeline',
        '--config',
        '/fefs/aswg/lstosa/cfg/sequencer_v0.11.cfg',
        '--date=2025-07-02',
        '--drs4-pedestal-run=20993',
        '--pedcal-run=20994',
        'LST1'
    ])

sys.exit(proc.returncode)
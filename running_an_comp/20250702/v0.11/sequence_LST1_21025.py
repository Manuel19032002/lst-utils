#!/bin/env python

#SBATCH --job-name=LST1_21025
#SBATCH --time=2:00:00
#SBATCH --chdir=/fefs/onsite/data/lst-pipe/LSTN-01/running_analysis/20250702/v0.11
#SBATCH --output=log/Run21025.%4a_jobid_%A.out
#SBATCH --error=log/Run21025.%4a_jobid_%A.err
#SBATCH --array=0-87
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
subruns = int(os.getenv('SLURM_ARRAY_TASK_ID'))

with tempfile.TemporaryDirectory() as tmpdirname:
    os.environ['NUMBA_CACHE_DIR'] = tmpdirname
    proc = subprocess.run([
        'datasequence',
        '--config',
        '/fefs/aswg/lstosa/cfg/sequencer_v0.11.cfg',
        '--date=2025-07-02',
        '--prod-id=v0.11',
        '--drs4-pedestal-file=/fefs/onsite/data/lst-pipe/LSTN-01/monitoring/PixelCalibration/Cat-A/drs4_baseline/20250702/v0.1.1/drs4_pedestal.Run20993.0000.h5',
        '--time-calib-file=/fefs/aswg/data/real/monitoring/PixelCalibration/Cat-A/drs4_time_sampling_from_FF/20250326/v0.10.18/time_calibration.Run20529.0000.h5',
        '--pedcal-file=/fefs/onsite/data/lst-pipe/LSTN-01/monitoring/PixelCalibration/Cat-A/calibration/20250702/v0.1.1/calibration_filters_52.Run20994.0000.h5',
        '--systematic-correction-file=/fefs/aswg/data/real/monitoring/PixelCalibration/Cat-A/ffactor_systematics/20230410/v0.10.3/calibration_scan_fit_20230410.0000.h5',
        '--drive-file=/fefs/onsite/monitoring/driveLST1/DrivePositioning/DrivePosition_log_20250702.txt',
        '--run-summary=/fefs/onsite/data/lst-pipe/LSTN-01/monitoring/RunSummary/RunSummary_20250702.ecsv',
        '--dl1b-config=/fefs/aswg/data/real/auxiliary/TailCuts/dl1ab_Run21025.json',
        '--dl1-prod-id=tailcut84',
        f'21025.{subruns:04d}',
        'LST1'
    ])

sys.exit(proc.returncode)
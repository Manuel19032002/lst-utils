import os
import tarfile
import pathlib
import logging
import argparse
from datetime import datetime

# =================================================================
# CONFIGURATION
# =================================================================

# Multiple patterns: list of tuples (file_pattern, tar_name)
# Each tuple contains: (glob_pattern, prefix_for_tar_gz)
FILE_PATTERNS = [
    ("g*.log", "GainSel_log"),
    ("e*.log", "ErrorLog"),
    ("s*.dat", "SensorData"),
    # Add more patterns as needed
]

BASE_PATH = "."              # Starting directory
SIMULATION = False           # CHANGE TO False TO DELETE FOR REAL
LOG_FILE = "cleanup_log.log"
# =================================================================

# Log system configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def format_size(bytes_size):
    """Makes bytes human-readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"


def run_cleanup(dir_pattern):
    base_path = pathlib.Path(BASE_PATH)
    directories = [d for d in base_path.glob(dir_pattern) if d.is_dir()]
    
    if not directories:
        print(f"No folders found with pattern: {dir_pattern}")
        return

    total_freed = 0
    print(f"🚀 {'SIMULATION' if SIMULATION else 'REAL'} mode active")
    print(f"📝 Log: {LOG_FILE} | Compression: GZIP")
    print(f"📋 Configured patterns: {len(FILE_PATTERNS)}")
    print("-" * 60)
    logging.info(f"--- NEW SESSION (Simulation: {SIMULATION}) ---")

    for folder in directories:
        print(f"📁 Directory: {folder.name}")
        
        for file_pattern, name_prefix in FILE_PATTERNS:
            files = list(folder.glob(file_pattern))
            
            if not files:
                continue

            # Define the compressed file name
            compressed_name = folder / f"{folder.name}_{name_prefix}.tar.gz"
            current_size = sum(f.stat().st_size for f in files)
            
            print(f"  └─ Pattern '{file_pattern}' | {len(files)} files | {format_size(current_size)}")

            if SIMULATION:
                logging.info(f"[SIM] Would process {len(files)} files ({file_pattern}) in {folder.name}")
                print(f"     [SIM] Would create {compressed_name.name}")
            else:
                try:
                    # 'w:gz' to create a Gzip compressed file
                    with tarfile.open(compressed_name, "w:gz") as tar:
                        for f in files:
                            tar.add(f, arcname=f.name)
                    
                    # Safe deletion: only happens if tar closed properly
                    for f in files:
                        f.unlink()
                    
                    total_freed += current_size
                    print(f"     ✅ Compressed and freed.")
                    logging.info(f"SUCCESS: {folder.name} ({file_pattern}) compressed. {len(files)} files deleted.")
                    
                except Exception as e:
                    error_msg = f"ERROR in {folder.name} ({file_pattern}): {str(e)}"
                    print(f"     ❌ {error_msg}")
                    logging.error(error_msg)
        
        print("-" * 60)

    summary = f"FINISHED. Total space recovered: {format_size(total_freed)}"
    print(summary)
    logging.info(summary)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compress files in specific folders.')
    parser.add_argument('dir_pattern', 
                        help='Target folder pattern (e.g.: 20260215 or 2026*)',
                        default='20260215',
                        nargs='?')
    
    args = parser.parse_args()
    run_cleanup(args.dir_pattern)
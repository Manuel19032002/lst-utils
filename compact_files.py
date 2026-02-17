import argparse
import os

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Process some directories.')
parser.add_argument('--patron_dir', type=str, help='Path to the patron directory', required=True)

args = parser.parse_args()

# Use PATRON_DIR from command line argument
PATRON_DIR = args.patron_dir

# Your existing code logic here using PATRON_DIR instead of hardcoded value



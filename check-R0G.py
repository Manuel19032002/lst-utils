#!/bin/env python

import os

directory1 = '/fefs/onsite/data/R0/LSTN-01/lst-arraydaq/events'
directory2 = '/fefs/onsite/data/lst-pipe/LSTN-01/R0G'

subdirectories1 = [d for d in os.listdir(directory1) if os.path.isdir(os.path.join(directory1, d))]
subdirectories2 = [d for d in os.listdir(directory2) if os.path.isdir(os.path.join(directory2, d))]

#print(f'Subdirectories in {directory1}: {subdirectories1}')
#print(f'Subdirectories in {directory2}: {subdirectories2}')

subdirectories1_set = set(subdirectories1)
subdirectories2_set = set(subdirectories2)

common_subdirectories = list(subdirectories1_set.intersection(subdirectories2_set))
common_subdirectories.sort()
not_common_subdirectories = list(subdirectories1_set^subdirectories2_set)

print(f"Common subdirectories: {common_subdirectories}")
print(f"Different  subdirectories: {not_common_subdirectories}")



file_counts = {}

for subdirectory in common_subdirectories:
    full_path1 = os.path.join(directory1, subdirectory)
    full_path2 = os.path.join(directory2, subdirectory)

    count1 = 0
    if os.path.exists(full_path1) and os.path.isdir(full_path1):
        count1 = len([entry for entry in os.listdir(full_path1) if os.path.isfile(os.path.join(full_path1, entry))])

    count2 = 0
    if os.path.exists(full_path2) and os.path.isdir(full_path2):
        count2 = len([entry for entry in os.listdir(full_path2) if os.path.isfile(os.path.join(full_path2, entry))])

    file_counts[subdirectory] = (count1, count2)

    print(subdirectory,file_counts[subdirectory])

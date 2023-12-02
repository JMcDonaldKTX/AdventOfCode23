#### From Landcruiser87 at https://github.com/Landcruiser87/AoC2023/blob/main/utils/

import os, sys

def recurse_dir(dir = './'):
    count = 0

    for file in os.listdir(dir):
        if not os.path.isfile(dir + file):
            count += recurse_dir(dir + file + '/')
        elif file.endswith('.py'):
            with open(dir + file, 'r') as f:
                for line in f.read().split('\n'):
                    if (not line.strip().startswith('#')) and (not line.strip() == ''):
                        count += 1

    return count

# to use pass file directory into function call
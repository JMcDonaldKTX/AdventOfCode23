#### From Landcruiser87 at https://github.com/Landcruiser87/AoC2023/blob/main/utils/

import pandas as pd
import re
import os
import sys
from utils.time_run import log_time
from utils.loc import recurse_dir

# template and util functions (loc and time_run) from Landcruiser87

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

DAY = './AdventOfCode/day2/'
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}.txt', 'r') as f:
		data = f.read().splitlines()
		arr = [x if x != "" else "" for x in data]
	return arr

@log_time
def run_part_A():
	data = data_load()


@log_time
def run_part_B():
	data = data_load()
	
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes
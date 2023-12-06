#import pandas as pd
import re
import os
import sys
from typing import Tuple, List
import numpy as np

# template and util functions (loc and time_run) from Landcruiser87

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
from utils.time_run import log_time
from utils.loc import recurse_dir

DIGITS = re.compile(r'\d+')
SYMBOLS = re.compile(r'[^\.\d]')

DAY = 'day6\\'
def data_load(filen:str)->list:
    with open(f'{DAY}{filen}', 'r') as f:
        data = f.read().splitlines()
        arr = [x if x != "" else "" for x in data] 
    return arr


def process_data(data:list)->int:
    t_r = []
    val = 1
    count = 0
    for line in data:
        t_r.append(re.findall(DIGITS, line))
    for i in range(0, 4):
        count = 0
        for j in range(1, int(t_r[0][i])+1):
            if ((int(t_r[0][i])-j) * j) > int(t_r[1][i]):
                count +=1
        if count > 0:
            val = val * count
    return val

def process_data_2(data:list)->int:
    t_r = []
    val = 1
    count = 0
    for line in data:
        t_r.append(''.join(re.findall(DIGITS, line)))
    for i in range(0, 1):
        start = 0
        for j in range(int(start), int(t_r[0])):
            if (j * (int(t_r[0])-j)) > int(t_r[1]):
                start+=1
    print(start)
    return start



@log_time
def run_part_A()->int:
    data = data_load('day6.txt')
    min_loc = process_data(data)
    return min_loc


@log_time
def run_part_B():
    data = data_load('day6.txt')
    min_loc = process_data_2(data)
    return min_loc
    
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")
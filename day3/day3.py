import pandas as pd
import re
import os
import sys
from typing import Tuple

# template and util functions (loc and time_run) from Landcruiser87

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)


from utils.time_run import log_time
from utils.loc import recurse_dir

#I hate regex but crap its useful...
DIGITS = re.compile(r'\d+')
SYMBOLS = re.compile(r'[^\.\d]')

DAY = '/AdventOfCode23/day3/'
def data_load(filen:str)->list:
    with open(f'{DAY}{filen}', 'r') as f:
        data = f.read().splitlines()
        arr = [f'.{x}.' if x != "" else "" for x in data] #added .{x}. to help with anything where a * was on the edge in part 2
    return arr

def find_nums(data:list) -> Tuple[list, dict]:
    nums = []
    loc = {}
    for i, row in enumerate(data):
        for item in re.finditer(DIGITS, row):
            index = len(nums)
            nums.append(int(item.group()))
            for j in range(item.start(), item.end()):
                loc[i,j] = index
    return nums, loc

def process_data(data:list)->int:
    nums, loc = find_nums(data)
    part_nums = set()
    for k, row in enumerate(data):
        for item in re.finditer(SYMBOLS, row):
            for l in range(k - 1, k + 2):
                for m in range(item.start() - 1, item.start() + 2):
                    if loc.get((l,m),-1) != -1:
                        part_nums.add(loc[l,m])
    return sum([nums[i] for i in part_nums])


def process_data_2(data:list)->int:
    nums, loc = find_nums(data)
    gear_ratio = 0
    for k,row in enumerate(data):
        for item in re.finditer(SYMBOLS, row):
            gear = set()
            for l in range(k - 1, k + 2):
                for m in range(item.start() - 1, item.start() + 2):
                    if loc.get((l,m),-1) != -1:
                        gear.add(loc[l,m])
            if len(gear) == 2:
                gear_ratio += nums[gear.pop()] * nums[gear.pop()] 
    return gear_ratio


@log_time
def run_part_A()->int:
    data = data_load('day3.txt')
    games = process_data(data)
    return games


@log_time
def run_part_B():
    data = data_load('day3.txt')
    power = process_data_2(data)
    return power
    
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")
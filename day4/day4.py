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

DIGITS = re.compile(r'\d+')
SYMBOLS = re.compile(r'[^\.\d]')

DAY = '/AdventOfCode23/day4/'
def data_load(filen:str)->list:
    with open(f'{DAY}{filen}', 'r') as f:
        data = f.read().splitlines()
        arr = [x if x != "" else "" for x in data] 
    return arr

def score_cards(data:list)-> Tuple[int, dict]:
    total = 0
    loc = {}
    for idx, row in enumerate(data):
        row = data[idx][8:].split('|')
        nums = {}
        for i, r in enumerate(row):
            cur_nums = set()
            for item in re.finditer(DIGITS, r):
                cur_nums.add(int(item.group()))
            nums[i] = cur_nums
        inter = nums[0].intersection(nums[1])
        exp = len(inter) - 1
        loc[idx+1] = len(inter)
        if exp >= 0:
            total += 2**exp
    return total, loc

def process_data(data:list)->int:
    total, loc = score_cards(data)
    return total

def process_data_2(data:list)->int:
    total, loc = score_cards(data)
    max = len(loc)
    total = 0
    count_cards = {}
    for init in range(1,194):
        count_cards[init] = 1
    #print(loc)
    for k, v in loc.items():
        for p in range(1, v+1):
            for r in range(count_cards.get(k)):
                if k < max:
                    count_cards[k+p] = (count_cards.get(k+p) + 1)
    return sum(count_cards.values())




@log_time
def run_part_A()->int:
    data = data_load('day4.txt')
    games = process_data(data)
    return games


@log_time
def run_part_B():
    data = data_load('day4.txt')
    power = process_data_2(data)
    return power
    
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")
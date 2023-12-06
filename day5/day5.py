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
MAP = ['seeds', 'seed-to-soil map', 'soil-to-fertilizer map', 'fertilizer-to-water map', 'water-to-light map', 'light-to-temperature map', 'temperature-to-humidity map', 'humidity-to-location map']

DAY = 'day5\\'
def data_load(filen:str)->list:
    with open(f'{DAY}{filen}', 'r') as f:
        data = f.read().splitlines()
        arr = [x if x != "" else "" for x in data] 
    return arr

def map_seeds(data:list)-> Tuple[list, dict]:
    seed_list_1 = []
    seed_list_2 = []
    cat_map = {} #thinking a dict that contains lists that contain tuples...
    cur_cat = ""
    for idx, row in enumerate(data):
        map_bank = [] #now I'm just making up names because I'm running out
        if row.startswith('seeds:'):
            for item in re.finditer(DIGITS, row):
                seed_list_1.append(int(item.group()))
            #may not need the full seed list 2 since that would be computationally expensive
            for s in range(0, len(seed_list_1), 2):
                seed_list_2.append((seed_list_1[s], seed_list_1[s]+seed_list_1[s+1]))
        else:
            try:
                if row[0].isalpha():
                    cat = row.split(' ')[0]
                    cur_cat = cat.split('-')[2]
                    last_cat = cat.split('-')[0]
                    cat_map[cat] = np.empty((0,3), int)
                elif row[0].isdigit():
                    line = []
                    for item in re.finditer(DIGITS, row):
                        line.append(int(item.group()))
                    cat_map[cat] = np.append(cat_map[cat], [line], axis=0)
                    #this loop was creating an entire output of all teh possible combinations, which isn't neccessary and is computationally unimaginable!
                    #for j in range(0, line[2]):
                    #    cur_val = {'Source':line[1] + j, 'Destination': line[0] + j}
                    #    cat_map[cat] = pd.concat([cat_map[cat],pd.Series(cur_val).to_frame().T], ignore_index=True)
            #handling the blank line with a try except like an idiot
            except Exception as e:
                #print(e)
                pass
        seed_list = [seed_list_1, seed_list_2] #leaving this in as is for now but approaching a different way
    return seed_list, cat_map
                    
def lookup(mapping: np.array, val: int)->int:
    # need to find which mapping addresses this seed for this map-attribute-list
    #maybe sort the list and get the one where the seed is between the source and source+range, then return dest + range - (seed-source)
    for x in mapping:
        if val >= x[1] and val <= (x[1] + x[2]):
            return (x[0] + (val - x[1]))
    return val
    return 0

def lookup_2(mapping:List[list],seeds:List[Tuple[int, int]])->List[Tuple[int, int]]:
    # need to handle when the max seed exceeds the range of seeds, set seed to seed + range, then loop back until it doesn't and search again
    last_seed = False
    final_seeds = []

    imp_seeds = []
    for dest, source, range in mapping:
        dest_to_source = dest - source
        max_seed = source + range
        seeds_left = []
        try:
            for begin, end in seeds:
                if source <= begin < end <= max_seed:
                    final_seeds.append((begin + dest_to_source, end + dest_to_source))
                elif begin < source < end <= max_seed:
                    seeds_left.append((begin, source))
                    final_seeds.append((source + dest_to_source, end + dest_to_source))
                elif source <= begin < max_seed < end:
                    seeds_left.append((max_seed, end))
                    final_seeds.append((begin + dest_to_source, max_seed + dest_to_source))
                elif begin < source <= max_seed < end:
                    seeds_left.append((begin, source))
                    seeds_left.append((max_seed, end))
                    final_seeds.append((source + dest_to_source, max_seed + dest_to_source))
                else: #if the seed didn't fit in anywhere....a bad seed
                    seeds_left.append((begin, end))
                #print(seeds_left)
        except: #get an error when the seeds are empty though I'm not sure why the error that is throw is thrown...but og well
            seeds = seeds_left
    final_seeds.extend(seeds_left)
    return final_seeds



def process_data(data:list)->int:
    seeds, map = map_seeds(data)
    min_val = 10000000000000000000000000000 #just a big number to go for min ...and don't wanna do an if == 0
    for seed in seeds[0]:
        cur_val = seed
        for k,v in map.items():
            cur_val = lookup(map[k], cur_val) #sends the 
        min_val = min(min_val, cur_val)
        
    # for k,v in map.items():
    #     print(k)
    #     print(v)
    return min_val

def process_data_2(data:list)->int:
    #returns a list of seeds and max_seeds, and a dict of catergories with the mappings contained
    seed_list, mappings = map_seeds(data)
    last_seed = False
    #print(seed_list[1])
    for k, v in mappings.items():
        seed_list[1] = lookup_2(v, seed_list[1])
    return(min(seed_list[1])[0])


@log_time
def run_part_A()->int:
    data = data_load('day5test.txt')
    min_loc = process_data(data)
    return min_loc


@log_time
def run_part_B():
    data = data_load('day5.txt')
    min_loc = process_data_2(data)
    return min_loc
    
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")
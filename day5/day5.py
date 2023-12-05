#import pandas as pd
import re
import os
import sys
from typing import Tuple
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
                seed_list_2.append((seed_list_1[s], seed_list_1[s+1]))
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

def lookup_2(mapping: np.array, val, seed: int, max_seed:int)->int:
    # need to handle when the max seed exceeds the range of seeds, set seed to seed + range, then loop back until it doesn't and search again
    pot_max = val
    seed = seed
    mapping = mapping[mapping[:,1].argsort()]
    cur_mins = []
    for x in mapping:
        for d, s, r in x:
            max_n = max(seed, s)
            min_n = min(pot_max, s + r)
            if max_n < min_n:
                cur_mins.append(max_n - s + d, min_n - s + d)
                #if max_n > seed:
                        
                
    #     #print(f'seed: {seed}, max_seed: {max_seed}, x: {x}')
    #     if (seed >= x[1] and seed <= (x[1] + x[2])) and (max_seed >= x[1] and max_seed <= (x[1] + x[2])):
    #         return (x[0] + (seed - x[1]))
    #     elif (seed >= x[1] and seed <= (x[1] + x[2])):
            
    #         seed = (x[1] + x[2]) + 1
    #         continue
    # #print('returning seed')            
    return seed
    #return 0

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
    seed_list, mappings = map_seeds(data)
    #min_val = 10000000000000000000000000000000000000000000000000000000000000000000000000000000 #just a big number to go for min ...and don't wanna do an if == 0
    #print(seeds[1])
    seeds = seed_list[1]
    seeds.reverse()
    for k,v in mappings.items():
        cur_cat = mappings[k]
        next_s = []
        print(seeds[0])
        while len(seeds) > 0:
            seed, max_seed = seeds.pop()
            for d, s, r in cur_cat:
                max_s = max(seed, s)
                min_max = min(max_seed, s + r)
                if max_s < min_max:
                    next_s.append((max_s - s + d, min_max - s + d))
                    if max_s > seed:
                        seeds.append((seed, max_s))
                    if max_seed > min_max:
                        seeds.append((min_max, max_seed))   
                    break
                else:
                    next_s.append((seed, max_seed))
        seeds = next_s
    return(min(seeds)[0])
    # for s in range(0, len(seeds), 2):
    #     cur_val = seeds[s]
    #     max_seed = cur_val + seeds[s+1]
    #     #print(f'{cur_val}   {max_seed}')
    #     for k,v in mapping.items():
    #         cur_val = lookup_2(mapping[k], cur_val, seeds[s], max_seed) #sends the 
    #         print(cur_val)
    #     min_val = min(min_val, cur_val)
    
    # for k,v in mapping.items():
    #     print(k)
    #     print(v)
    return min_val




@log_time
def run_part_A()->int:
    data = data_load('day5test.txt')
    games = process_data(data)
    return games


@log_time
def run_part_B():
    data = data_load('day5test.txt')
    power = process_data_2(data)
    return power
    
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")
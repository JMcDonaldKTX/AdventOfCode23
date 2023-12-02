import pandas as pd
import re
import os
import sys

# template and util functions (loc and time_run) from Landcruiser87

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)


from utils.time_run import log_time
from utils.loc import recurse_dir

DAY = '/AdventOfCode23/day2/'
def data_load(filen:str)->list:
	with open(f'{DAY}{filen}', 'r') as f:
		data = f.read().splitlines()
		arr = [x if x != "" else "" for x in data]
	return arr

#part 1
def check_game(line:str)->int:
	clean_ln = line[line.rfind(':') + 1: ]
	draws = clean_ln.split(';')
	for draw in draws:
		colors = draw.split(',')
		for color in colors:
			cnt_clr = color.strip().split(' ')
			if cnt_clr[1].strip() == 'red':
				if int(cnt_clr[0].strip()) > 12:
					return 0
			elif cnt_clr[1].strip() == 'green':
				if int(cnt_clr[0].strip()) > 13:
					return 0
			elif cnt_clr[1].strip() == 'blue':
				if int(cnt_clr[0].strip()) > 14:
					return 0
	game = line[:line.rfind(':')]
	return int(game.strip().split(' ')[1])

def each_game(data:list)->int:
	game_sum = 0
	for line in data:
		check = check_game(line)
		game_sum = game_sum + check
	return game_sum
	
#part two		
def check_game_2(line:str)->int:
	red = 1
	green = 1
	blue = 1
	clean_ln = line[line.rfind(':') + 1: ]
	draws = clean_ln.split(';')
	for draw in draws:
		colors = draw.split(',')
		for color in colors:
			cnt_clr = color.strip().split(' ')
			if cnt_clr[1].strip() == 'red':
				if int(cnt_clr[0].strip()) > red:
					red = int(cnt_clr[0])
			elif cnt_clr[1].strip() == 'green':
				if int(cnt_clr[0].strip()) > green:
					green = int(cnt_clr[0])
			elif cnt_clr[1].strip() == 'blue':
				if int(cnt_clr[0].strip()) > blue:
					blue = int(cnt_clr[0])
	
	return red*green*blue

def each_game_2(data:list)->int:
	power = 0
	for line in data:
		check = check_game_2(line)
		power = power + check
	return power

@log_time
def run_part_A()->int:
	data = data_load('day2.txt')
	games = each_game(data)
	return games


@log_time
def run_part_B():
	data = data_load('day2.txt')
	power = each_game_2(data)
	return power
	
print(f"Part A solution: \n{run_part_A()}\n")
print(f"Part B solution: \n{run_part_B()}\n")
print(f"Lines of code \n{recurse_dir(DAY)}")

########################################################
#Notes
#Part A Notes
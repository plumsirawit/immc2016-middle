# main.py -- Python file for main simulation.
from scipy import stats
from util import *
contestant_per_country = 2

dat = [(0,0,'','',0)]
with open('immc2016-data.csv') as f:
	for line in f:
		cdat = line.strip().split(',')
		cdat[0] = int(cdat[0])
		cdat[1] = int(cdat[1])
		cdat[4] = int(cdat[4])
		dat.append(cdat)
print(dat)
def calculate(window):
	
def simulate(c1, c2, c3):
	qs = [0]
	country_win_count = {}
	for stats in dat:
		country_win_count[stats[3]] = 0
	last_winner_country = ''
	last_winner_name = ''
	for i in range(1,len(dat)):
		slope = stats.linregress(list(range(i)),qs)[0]
		current_window = []
		for j in country_list:
			buf = country_win_count[j] + c3
			current_window.append((j,buf,'Anonymous'))
			if last_winner_country == j:
				buf += c1 * streak
			current_window.append((j,buf,last_winner_name))
		calculate(current_window)
		qs.append(qs[-1] + dat[i][4])
		country_win_count[dat[i][3]] += 1
		

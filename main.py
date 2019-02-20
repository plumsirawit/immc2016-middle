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
def simulate(c1, c2, c3):
	qs = [0]
	for i in range(1,len(dat)):
		qs.append(qs[-1] + dat[i][4])
		slope = stats.linregress(list(range(i+1),qs))[0]
		

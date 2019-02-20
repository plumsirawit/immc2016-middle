# main.py -- Python file for main simulation.
import scipy.stats
import numpy as np

dat = [(0,0,'','',0)]
with open('immc2016-data.csv') as f:
	for line in f:
		cdat = line.strip().split(',')
		cdat[0] = int(cdat[0])
		cdat[1] = int(cdat[1])
		cdat[4] = int(cdat[4])
		dat.append(cdat)

def calculate(window):
	k = [0.0 for i in window]
	for i in range(len(window)):
		k[i] = window[i][1]
	s = sum(k)
	for i in range(len(k)):
		k[i] /= s
	return window[np.random.choice(list(range(len(window))),p=k)]

ncnt = 0
def newname():
	global ncnt
	ncnt += 1
	return str(ncnt)

def simulate(c1, c2, c3):
	qs = [0]
	country_win_count = {}
	for stats in dat:
		country_win_count[stats[3]] = 0
	last_winner_country = ''
	last_winner_name = ''
	streak = 0
	prediction = []
	qs.append(qs[0] + 1)
	country_win_count[dat[1][3]] += 1
	for i in range(2,len(dat)):
		slope = scipy.stats.linregress(list(range(i)),qs)[0]
		current_window = []
		for j in country_win_count.keys():
			buf = float(country_win_count[j]) + c3
			current_window.append((j,buf,newname()))
			if last_winner_country == j:
				buf += c1 * float(streak)
			current_window.append((j,buf,last_winner_name))
		current_winner = calculate(current_window)
		if i <= 15:
			current_winner = (dat[i][3],0,dat[i][2])
		if current_winner[0] == last_winner_country and current_winner[2] == last_winner_name:
			streak += 1
		else:
			streak = 0
		rate = slope * c2 ** qs[i-1]
		if rate > 1:
			rate = 1.0
		assert(0 <= rate <= 1)
		broken = np.random.choice([0,1],p=[1-rate,rate])
		if i <= 15:
			broken = dat[i][4]
		print('[DEBUG]','Slope:',slope,', Current Winner:', current_winner, ', Streak:', streak, ', Broken Rate:',rate,', Broken?:', broken)
		qs.append(qs[-1] + broken)
		country_win_count[current_winner[0]] += 1

# Main
simulate(0,1.1,0.5)




		

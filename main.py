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

def testCoeff(c1, c2, c3):
	qs = [0]
	country_win_count = dict.fromkeys({'Ethiopia': 11, 'Netherlands': 7, 'Kenya': 10, 'United Kingdom': 3, 'Belgium': 1, 'Ireland': 0, 'Morocco': 1, 'Norway': 0, 'Russia': 0, 'South Africa': 0}.keys(),0)
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
			else:
				current_window.append((j,buf,newname()))
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
		# Debug
		# print('[DEBUG]','Slope:',slope,', Current Winner:', current_winner, ', Streak:', streak, ', Broken Rate:',rate,', Broken?:', broken)
		if i > 15:
			prediction.append((i,current_winner[0],broken))
		qs.append(qs[-1] + broken)
		country_win_count[current_winner[0]] += 1
	return prediction

# Main
rescnt = 0

idealCase = {'Ethiopia': 11, 'Netherlands': 7, 'Kenya': 10, 'United Kingdom': 3, 'Belgium': 1, 'Ireland': 0, 'Morocco': 1, 'Norway': 0, 'Russia': 0, 'South Africa': 0}
bestTuple = (-1,-1,-1)
bestMistakes = 1000000
for c1 in range(0,1000,10):
	for c2 in range(100,200,10):
		for c3 in range(0,1000,100):
			with open('results/' + str(rescnt) + '.txt','w') as f:
				out = testCoeff(c1/100,c2/100,c3/100)
				mistakes = 0
				currentCase = dict.fromkeys(idealCase.keys(),0)
				for t in out:
					if dat[t[0]][4] != str(t[2]):
						mistakes += 1
					if t[1] not in currentCase:
						print('[DEBUG]',t,c1,c2,c3)
					else:
						currentCase[t[1]] += 1
				for key in idealCase.keys():
					mistakes += abs(idealCase[key] - currentCase[key])
				if mistakes < bestMistakes:
					bestMistakes = mistakes
					bestTuple = (c1/100,c2/100,c3/100)
				f.write('---\n')
				f.write('Iteration #')
				f.write(str(rescnt))
				f.write('\n')
				f.write('c1 : ')
				f.write(str(c1/100))
				f.write('\n')
				f.write('c2 : ')
				f.write(str(c2/100))
				f.write('\n')
				f.write('c3 : ')
				f.write(str(c3/100))
				f.write('\n')
				f.write('---\n')
				for res in out:
					f.write(str(res[0]))
					f.write(',')
					f.write(res[1])
					f.write(',')
					f.write(str(res[2]))
					f.write('\n')
				rescnt += 1
				print('Processing Iteration',rescnt)
print('Answer', bestTuple, bestMistakes)

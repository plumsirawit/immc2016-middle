# util.py -- Utility Module
import random
def weighted_random(r):
	# r is a list of pairs (value, weight)
	t = sum(p[1] for p in r)
	c = random.randint(1, t)
	for (v,w) in r:
		c -= w
		if r <= 0:
			return v
	else:
		raise ValueError('Unexpected Error')

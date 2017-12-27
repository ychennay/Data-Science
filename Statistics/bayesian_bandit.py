import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

NUM_TRIALS = 2000
BANDIT_PROBABILITIES = [0.2, 0.5, 0.6]

class Bandit:

	def __init__(self, p):
		self.p = p
		self.a = 1
		self.b = 1

	def pull(self):
		return np.random.random() < self.p

	def sample(self):
		beta_sample = np.random.beta(self.a, self.b)
		print("Beta sample for bandit {0}: {1}".format(self.p, beta_sample))
		return beta_sample

	def update(self, x):

		"""
		x must be either 0 or 1
		"""

		self.a += x
		print("a parameter for bandit {0} updated to {1}".format(self.p, self.a))
		self.b += 1 -x
		print("a parameter for bandit {0} updated to {1}".format(self.p, self.b))


def plot(bandits, trial):
	x = np.linspace(0,1,200)
	for b in bandits:
		y = beta.pdf(x, b.a, b.b)
		plt.plot(x, y, label = "Real p: {0}".format(b.p))
	plt.title("Bandit distributions after {0}".format(trial))
	plt.legend()
	plt.show()

def experiment():
	bandits = [Bandit(p) for p in BANDIT_PROBABILITIES]
	sample_points = [5, 10, 20, 50, 100, 500, 1000, 1999]

	for i in range(NUM_TRIALS):
		best_bandit = None # indicator for the best bandit machine
		maxsample = -1
		allsamples = []
		for bandit in bandits:
			sample = bandit.sample()
			allsamples.append(sample)
			if sample > maxsample:
				best_bandit = bandit
				maxsample = sample

		if i in sample_points:
			print("Current samples: {0}".format(allsamples))
			plot(bandits, i)

		print("The best current bandit is {0}".format(best_bandit.p))
		x = best_bandit.pull()
		best_bandit.update(x)

if __name__ == '__main__':
	experiment()

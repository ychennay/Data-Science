import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

class DataGenerator:

	@staticmethod
	def next(p1, p2):
		click1 = 1 if (np.random.random() < p1) else 0
		click2 = 1 if (np.random.random() < p2) else 0
		return click1, click2

	@staticmethod
	def get_p_value(T):
		determinant = T[0,0] * T[1,1] - T[0,1] * T[1,0]
		c2 = float(determinant) / T[0].sum() * determinant / T[1].sum() * T.sum() / T[:,0].sum() / T[:,1].sum()
		p = 1 - chi2.cdf(x = c2, df = 1)
		return p

	@staticmethod
	def run_experiment(N, p1, p2):

		p_values = np.empty(N)
		T = np.zeros((2,2)).astype(np.float32)

		for i in range(N):
			c1, c2 = DataGenerator.next(p1, p2)
			T[0,c1] += 1
			T[1,c2] += 1
			if i <= 10:
				p_values[i] = None
			else:
				p_values[i] = DataGenerator.get_p_value(T)

		plt.plot(p_values)
		plt.plot(np.ones(N) * 0.05)
		plt.show()

DataGenerator.run_experiment(20000, 0.10, 0.11)
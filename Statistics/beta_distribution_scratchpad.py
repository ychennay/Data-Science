import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

iterations = 100


def spike(a):

	return a * 2

def test_beta(inc_a = 1, inc_b = 1, iterations= 500):

	a = 1.0
	b = 1.0
	vars = []
	count = 0

	for i in range(iterations):

		count += 1

		if np.random.random(1) < 0.01:
			a = spike(a)
			print("Spiking alpha parameter for test {0}: {1}".format(inc_a, inc_b))
			plt.axvline(count)

		else:
			a += inc_a
		b += inc_b
		var = (a * b) / (((a + b) ** 2) * (a + b + 1))
		vars.append(var)

	plt.plot(range(len(vars)), vars, label= "a: {0} b: {1}".format(inc_a, inc_b))

	return vars

vars1 = test_beta(.1,.2)
# vars2 = test_beta(1,2)
# vars3 = test_beta(2,2)
# vars4 = test_beta(2,1)
# vars5 = test_beta(0.5,0.5)
# vars6 = test_beta(3,1)
plt.legend()
plt.show()
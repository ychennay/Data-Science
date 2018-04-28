from scipy import linspace
from scipy import pi,sqrt,exp
from scipy.special import erf
from scipy.stats import describe, skewnorm
from pylab import plot,show

n = 10000


x = linspace(-100,100,n) 
a = -20

p = skewnorm.pdf(x, a, loc=50.4, scale=30)

print(describe(p))

plot(x,p)

show()
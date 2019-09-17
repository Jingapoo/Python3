import numpy as np
from numpy import sqrt
import numpy
from numpy import sum as arraysum
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import sys
import statsmodels.api as sm


df = pd.read_csv("AutoData3.csv")
x = df["horsepower"]
y = df["mpg"]
denominator = x.dot(x) - x.mean()* x.sum()
m = (x.dot(y) - y.mean() * x.sum())/denominator
b = (y.mean()* x.dot(x) - x.mean() * x.dot(y))/denominator
yPred = m * x + b
print(m, b)
'''The horsepower is 98
ninetyEightHP = m * 98.0 + b
print(str(ninetyEightHP))
sys.exit(0)
'''
#OLS table summary
X = sm.add_constant(x)
smModel = sm.OLS(y,X)
results = smModel.fit()
print(results.summary())
#95% confidence interval
print(results.conf_int(alpha=0.05, cols=None))
#prediction interval
x_in = x[0]
y_out = y[0]
yPred_out = yPred[0]
sum_errs = arraysum((y - yPred)**2)
stdev = sqrt(1/(len(y)-2) * sum_errs)
# calculate prediction interval
interval = 1.96 * stdev
print('Prediction Interval: %.3f' % interval)
lower, upper = y_out - interval, y_out + interval
print('95%% likelihood that the true value is between %.3f and %.3f' % (lower, upper))
print('True value: %.3f' % yPred_out)

plt.title("MPG vs Horsepower")
plt.xlabel("Horsepower")
plt.ylabel("MPG")
plt.scatter(x,y,color="blue")
plt.plot(x,yPred,'r',color="red", linewidth=3)
plt.show()

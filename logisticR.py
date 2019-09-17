import numpy as np
from numpy import median
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplot,figure,subplots
import sys
import statsmodels.api as sm
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

df = pd.read_csv("AutoData3.csv")
#print(df.head())

mpg01 = []
theMedian = median(df["mpg"])
for mpg in df["mpg"]:
    if mpg > theMedian:
        mpg01.append(1)
    else:
        mpg01.append(0)

'''
f1,axes = plt.subplots(3,3)
axes[0,0].scatter(df["cylinders"],mpg01, s = 3)
axes[0,0].set_title('Cylinders')
axes[1,0].scatter(df["displacement"],mpg01, s = 3)
axes[1,0].set_title('Displacement')
axes[0,1].scatter(df["horsepower"],mpg01, s = 3)
axes[0,1].set_title('Horsepower')
axes[1,1].scatter(df["weight"],mpg01, s = 3)
axes[1,1].set_title('Weight')
axes[2,0].scatter(df["acceleration"],mpg01, s = 3)
axes[2,0].set_title('Acceleration')
axes[2,1].scatter(df["year"],mpg01, s = 3)
axes[2,1].set_title('Year')
axes[2,2].scatter(df["origin"],mpg01, s = 3)
axes[2,2].set_title('Origin')
axes[0,2].scatter(df["mpg"],mpg01, s = 3)
axes[0,2].set_title('mpg')
f1.show()


f2,axes = plt.subplots(3,3)
axes[0,0].boxplot(df["cylinders"],0,'gD')
axes[0,0].set_title('Cylinders')
axes[1,0].boxplot(df["displacement"],0,'gD')
axes[1,0].set_title('Displacement')
axes[0,1].boxplot(df["horsepower"],0,'gD')
axes[0,1].set_title('Horsepower')
axes[1,1].boxplot(df["weight"],0,'gD')
axes[1,1].set_title('Weight')
axes[2,0].boxplot(df["acceleration"],0,'gD')
axes[2,0].set_title('Acceleration')
axes[2,1].boxplot(df["year"],0,'gD')
axes[2,1].set_title('Year')
axes[2,2].boxplot(df["origin"],0,'gD')
axes[2,2].set_title('Origin')
axes[0,2].boxplot(df["mpg"],0,'gD')
axes[0,2].set_title('mpg')
f2.show()

#Train/Test Split
'''
y = mpg01
X = sm.add_constant(df[["horsepower","cylinders","weight","displacement"]])
logit = sm.Logit(y, X.astype(float))
result = logit.fit()
print(result.summary())
#model fitting
cols = ["horsepower","cylinders","weight","displacement"]
X=df[cols]
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)
logreg = LogisticRegression()
logreg.fit(X_train,y_train)
yPred = logreg.predict(X_test)
print("Accuracy of Logistic regression classifier on test set:{:.2f}".format(logreg.score(X_test,y_test)))
#plt.show()

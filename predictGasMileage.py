import numpy as np
from numpy import median
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC

def mergeuh(a, b):
    merged = []
    i = 0
    length = len(a)
    if(length != len(b)):
        raise ValueError('Length of array a and b do not match.')
        return None
    while i < length:
        merged.append([a[i], b[i]])
        i = i + 1
    return merged

df = pd.read_csv("Auto.csv")
#print(df.head())
mpg01 = []
theMedian = median(df["mpg"])
for mpg in df["mpg"]:
    if mpg > theMedian:
        mpg01.append(1)
    else:
        mpg01.append(0)

plt.scatter(df["cylinders"], df["mpg"], marker="o",label="cylinders")
plt.scatter(df["displacement"],df["mpg"],marker="X",label="displacement")
plt.scatter(df["horsepower"],df["mpg"],marker="+",label="horsepower")
plt.scatter(df["weight"],df["mpg"],marker="s",label="weight")
plt.scatter(df["acceleration"],df["mpg"],marker="d",label="acceleration")
plt.scatter(df["year"],df["mpg"],marker="P",label="year")
plt.scatter(df["origin"],df["mpg"],marker="*",label="origin")
plt.legend(loc="upper right")
plt.title('predict gas mileage',fontname='Comic Sans MS', fontsize=18)
plt.xlabel("Attributes'value")
plt.ylabel("mpg")
plt.show()

cyl = np.array(mergeuh(df["cylinders"],df["mpg"]))
dis = np.array(mergeuh(df["displacement"],df["mpg"]))
hor = np.array(mergeuh(df["horsepower"],df["mpg"]))
wei = np.array(mergeuh(df["weight"],df["mpg"]))
acc = np.array(mergeuh(df["acceleration"],df["mpg"]))
year = np.array(mergeuh(df["year"],df["mpg"]))
orig = np.array(mergeuh(df["origin"],df["mpg"]))

#combing 2dim array into array([a,b],[c,d],...etc.)
X = np.concatenate((cyl,dis,hor,wei,acc,year,orig),axis=0)
#append more mpg01 to match the array
y = []
for a in mpg01:
    y.append(a)
for a in mpg01:
    y.append(a)
for a in mpg01:
    y.append(a)
for a in mpg01:
    y.append(a)
for a in mpg01:
    y.append(a)
for a in mpg01:
    y.append(a)
for a in mpg01:
    y.append(a)

#print(y)
'''
model = SVC(kernel="linear",C=1000).fit(X,y)
print(model.decision_function(X))
print(model.predict(X))
print('w = ',model.coef_) #only for linear
print('b = ',model.intercept_)
print('Indices of support vectors = ', model.support_)
print('Support vectors = ', model.support_vectors_)
print('Number of support vectors for each class = ', model.n_support_)
print('Coefficients of the support vector in the decision function = ',
        np.abs(model.dual_coef_))

model = SVC(kernel='rbf').fit(X,y) #Radial Basis Function(RBF)
print(model.decision_function(X))
print(model.predict(X))
print('b = ',model.intercept_)
print('Indices of support vectors = ', model.support_)
print('Support vectors = ', model.support_vectors_)
print('Number of support vectors for each class = ', model.n_support_)
print('Coefficients of the support vector in the decision function = ',
        np.abs(model.dual_coef_))
'''
model = SVC(kernel = "poly", degree=8).fit(X,y)#Polynomial Function
print(model.decision_function(X))
print(model.predict(X))
print('b = ',model.intercept_)
print('Indices of support vectors = ', model.support_)
print('Support vectors = ', model.support_vectors_)
print('Number of support vectors for each class = ', model.n_support_)
print('Coefficients of the support vector in the decision function = ',
        np.abs(model.dual_coef_))
'''
df = pd.read_csv("Auto.csv")
y = df["mpg"]
mpg01 = []
theMedian = median(df["mpg"])
for mpg in df["mpg"]:
    if mpg > theMedian:
        mpg01.append(1)
    else:
        mpg01.append(0)
#Cylinders vs mpg
plt.scatter(df[["cylinders"]],y,c=mpg01,s=30,cmap=plt.cm.get_cmap("winter",2))
plt.colorbar(ticks=range(2),label="mpg01 value")
plt.title('Cylinders vs.mpg',fontname='Comic Sans MS', fontsize=18)
plt.xlabel("Cylinders")
plt.ylabel("mpg")
plt.show()

#displacement vs mpg01
plt.scatter(df[["displacement"]],y,c=mpg01,s=30,cmap=plt.cm.get_cmap("winter",2))
plt.colorbar(ticks=range(2),label="mpg01 value")
plt.title('Displacement vs.mpg',fontname='Comic Sans MS', fontsize=18)
plt.xlabel("Displacement")
plt.ylabel("mpg")
plt.show()

#horsepower vs mpg01
plt.scatter(df["horsepower"],y,c=mpg01,s=30,cmap=plt.cm.get_cmap("winter",2))
plt.colorbar(ticks=range(2),label="mpg01 value")
plt.title('Horsepower vs.mpg',fontname='Comic Sans MS', fontsize=18)
plt.xlabel("Horsepower")
plt.ylabel("mpg")
plt.show()

#weight vs mpg01
plt.scatter(df[["weight"]],y,c=mpg01,s=30,cmap=plt.cm.get_cmap("winter",2))
plt.colorbar(ticks=range(2),label="mpg01 value")
plt.title('Weight vs.mpg',fontname='Comic Sans MS', fontsize=18)
plt.xlabel("Weight")
plt.ylabel("mpg")
plt.show()

#acceleration vs mpg01
plt.scatter(df[["acceleration"]],y,c=mpg01,s=30,cmap=plt.cm.get_cmap("winter",2))
plt.colorbar(ticks=range(2),label="mpg01 value")
plt.title('Acceleration vs.mpg',fontname='Comic Sans MS', fontsize=18)
plt.xlabel("Acceleration")
plt.ylabel("mpg")
plt.show()

#year vs mpg01
plt.scatter(df[["year"]],y,c=mpg01,s=30,cmap=plt.cm.get_cmap("winter",2))
plt.colorbar(ticks=range(2),label="mpg01 value")
plt.title('Year vs.mpg',fontname='Comic Sans MS', fontsize=18)
plt.xlabel("Year")
plt.ylabel("mpg")
plt.show()

#origin vs mpg01
plt.scatter(df[["origin"]],y,c=mpg01,s=30,cmap=plt.cm.get_cmap("winter",2))
plt.colorbar(ticks=range(2),label="mpg01 value")
plt.title('Origin vs.mpg',fontname='Comic Sans MS', fontsize=18)
plt.xlabel("Origin")
plt.ylabel("mpg")
plt.show()
'''

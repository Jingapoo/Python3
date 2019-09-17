import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

'''
#Remove the observations for whom the salary information is unknown
with open("Hitters.csv") as f:
    for line in f:
        row = line.split(',')
        if len(row[18]) > 0:
            print(line.replace("\n", ""))

#log transform the salaries
df = pd.read_csv("newHittersCopy.csv")
#print(df.head())
salary = df["Salary"]
log_salary = np.log(salary)
print ("log-transform the salaries:\n", log_salary)
#blue is salary before transformation
plt.plot(salary, salary,color = 'blue', marker = "*")
#red is salary after log transformation
plt.plot(log_salary, salary, color = 'red', marker = "o")
plt.title("Log transform the salaries")
plt.xlabel("log_array")
plt.ylabel("salary before transformation")
#plt.show()
'''
'''
#Gradient Boosting Regressor for training sets
df = pd.read_csv("hittersCopy.csv")
X = df.drop('Salary', axis = 1)#drop the column for prediction
#print(X)
X = np.array(X)
y = np.array(df["Salary"])#want to predict
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size = 0.25, random_state=42)
trainingError=[]
learningRate =[0.001,0.1,0.2,0.3,0.4,0.5]
for lr in learningRate:
    regr = GradientBoostingRegressor(max_depth=4, n_estimators=1000,learning_rate =lr,random_state=0)
    regr.fit(Xtrain, ytrain)
    prediction = regr.predict(Xtrain)
    trainingMSE = mean_squared_error(ytrain, prediction)
    trainingError.append(trainingMSE/100000)
learningRate =[0.001,0.1,0.2,0.3,0.4,0.5]
plt.plot(learningRate,trainingError)
plt.title("Gradient Boosting trainingMSE vs. Shrinkage")
plt.xlabel("Shrinkage")
plt.ylabel("Training Mean Squared Error(MSE)")
plt.show()
#Gradient Boosting Regressor for test sets
df = pd.read_csv("hittersCopy.csv")
X = df.drop('Salary', axis = 1)#drop the column for prediction
X = np.array(X)
y = np.array(df["Salary"])#want to predict
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size = 0.25, random_state=42)
testError=[]
learningRate =[0.001,0.1,0.2,0.3,0.4,0.5]
for lr in learningRate:
    regr = GradientBoostingRegressor(max_depth=4, n_estimators=1000,learning_rate =lr,random_state=0)
    #testMSE = np.mean(cross_val_score(regr, Xtest, ytest, cv=10,scoring = 'neg_mean_squared_error'))
    # Since this is neg_mean_squared_error I have inverted the sign to get MSE
    #testError.append(-testMSE/100000)
    regr.fit(Xtrain, ytrain)
    prediction = regr.predict(Xtest)
    testMSE = mean_squared_error(ytest, prediction)
    testError.append(testMSE/1000000)
learningRate =[0.001,0.1,0.2,0.3,0.4,0.5]
plt.plot(learningRate,testError)
plt.title("Gradient Boosting testMSE vs. Shrinkage")
plt.xlabel("Shrinkage")
plt.ylabel("Test Mean Squared Error(MSE)")
plt.show()
'''
#linear Regression
df = pd.read_csv("hittersCopy.csv")
X = df.drop('Salary', axis = 1)#drop the column for prediction
X = np.array(X)
y = np.array(df["Salary"])#want to predict

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size = 0.25, random_state=42)
'''
# Create linear regression object
linearR = LinearRegression()
# Train the model using the training sets
linearR.fit(Xtrain, ytrain)

# Make predictions using the testing set
prediction = linearR.predict(Xtest)
print("y-intercept: \n", linearR.intercept_)
# The coefficients
print('Coefficients: \n', linearR.coef_)
# The mean squared error
MSE = float(mean_squared_error(ytest, prediction))/1000000.00
print("Mean squared error: %.2f" % MSE)
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(ytest, prediction))
'''
testError = []
learningRate =[0.001,0.1,0.2,0.3,0.4,0.5]
for lr in learningRate:
    linearR = LinearRegression()
    linearR.fit(Xtrain, ytrain)
    prediction = linearR.predict(Xtest)
    testMSE = mean_squared_error(ytest, prediction)
    testError.append(testMSE/1000000.00)
learningRate =[0.001,0.1,0.2,0.3,0.4,0.5]
plt.plot(learningRate,testError)
plt.title("Linear Regression testMSE vs. Shrinkage")
plt.xlabel("Shrinkage")
plt.ylabel("Test Mean Squared Error(MSE)")
plt.show()

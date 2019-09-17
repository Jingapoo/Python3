import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from collections import OrderedDict

df = pd.read_csv("emailSpam.csv")
X = df.drop('spam', axis = 1)#drop the column for prediction

y = np.array(df["spam"])#want to predict
X = np.array(X)

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size = 0.25, random_state=42)
#print('Training Features Shape:', Xtrain.shape)#(3450, 57)
#print('Training Labels Shape:', ytrain.shape)#(3450, )
#print('Testing Features Shape:', Xtest.shape)#(1151, 57)
#print('Testing Labels Shape:', ytest.shape)#(1151,)

randomForest = RandomForestClassifier(n_estimators=1000, random_state=42)
randomForest.fit(Xtrain, ytrain)
prediction = randomForest.predict(Xtest)
#recall of the positive class is also known as “sensitivity”;
#recall of the negative class is “specificity”.
accuracy = accuracy_score(ytest,prediction)
print(metrics.classification_report(prediction, ytest))
print("accuracy:", accuracy)
print("Mean Squared Error is:", mean_squared_error(ytest,prediction))

'''
#Plot OOB and MSE Test Error
ensemble_clfs = [
    ("RandomForestClassifier, m = 'sqrt(p)'",
        RandomForestClassifier(n_estimators=100,
                               warm_start=True, oob_score=True,
                               max_features="sqrt",
                               random_state=123)),
    ("RandomForestClassifier, m = 'log2(p)'",
        RandomForestClassifier(n_estimators=100,
                               warm_start=True, max_features='log2',
                               oob_score=True,
                               random_state=123)),
    ("RandomForestClassifier, m = p",
        RandomForestClassifier(n_estimators=100,
                               warm_start=True, max_features=None,
                               oob_score=True,
                               random_state=123))
]
# Map a classifier name to a list of (<n_estimators>, <error rate>) pairs.
error_rate = OrderedDict((label, []) for label, _ in ensemble_clfs)

#print("Out-of-bag score is ",rfR.oob_score_)
# Range of `n_estimators` values to explore.
min_estimators = 15
max_estimators = 175

for label, clf in ensemble_clfs:
    for i in range(min_estimators, max_estimators + 1):
        clf.set_params(n_estimators=i)
        clf.fit(X, y)

        # Record the OOB error for each `n_estimators=i` setting.
        oob_error = 1 - clf.oob_score_
        error_rate[label].append((i, oob_error))

# Generate the "OOB error rate" vs. "n_estimators" plot.
for label, clf_err in error_rate.items():
    xs, ys = zip(*clf_err)
    plt.plot(xs, ys, label=label)

plt.xlim(min_estimators, max_estimators)
plt.title("OOB Error Rate Across various Forest sizes")
plt.xlabel("Number of trees")
plt.ylabel("OOB Error Rate")
plt.legend(loc="upper right")
plt.show()
'''

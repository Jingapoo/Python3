import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score as acc
from sklearn.ensemble import RandomForestClassifier
from mlxtend.feature_selection import SequentialFeatureSelector as sfs

df = pd.read_csv("house.csv")

X = df.values[:, 1:16]
Y = df.values[:, 17]
X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size = 0.3, random_state = 100)

#Build RF classifier to use in feature selection
clf = RandomForestClassifier(n_estimators = 100, n_jobs=-1)
#Build step forward feature selection
sfs1 = sfs(clf, k_features=5, forward=True,floating=False,verbose=2,scoring="accuracy",cv=5)
#Perform SFFS
sfs1 = sfs1.fit(X_train, y_train)
#which feature
featCols = list(sfs1.k_feature_idx_)
print("\n The following are the columns at theses indexes are those which were selected.")
print(featCols)
#Build full model with selected features
clf = RandomForestClassifier(n_estimators = 1000, random_state = 100, max_depth=4)
clf.fit(X_train[:,featCols],y_train)

yTrainPred=clf.predict(X_train[:,featCols])
print("Training accuracy on selected features: %.4f" % acc(y_train, yTrainPred))

yTestPred=clf.predict(X_test[:,featCols])
print("Testing accuracy on selected features: %.4f" % acc(y_test, yTestPred))

#Build full model on All features, for comparison
clf = RandomForestClassifier(n_estimators = 1000, random_state = 100, max_depth=4)
clf.fit(X_train,y_train)

yTPred=clf.predict(X_train)
print("Training accuracy on ALL features: %.4f" % acc(y_train, yTPred))

yTePred=clf.predict(X_test)
print("Testing accuracy on ALL features: %.4f" % acc(y_test, yTePred))

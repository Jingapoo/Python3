import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
from sklearn.svm import SVC #Support Vector Classifier
from sklearn.datasets.samples_generator import make_blobs
from sklearn.datasets.samples_generator import make_circles

sns.set()
#Kernel SVM, where SVM becomes extremely powerful is when it is combined with
#kernels, using this kernelized support vector machine, we learn a suitable
#nonlinear decision boundary. This kernel transformation strategy is used often
#in machine learning to turn fast linear methods into fast nonlinear methods,
#especially for models in which the kernel trick can be used.

X, y = make_circles(100, factor=.1, noise=.1)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
#plt.show()

model = SVC(kernel='linear').fit(X, y) #This is not work for linear
#model = SVC(kernel='rbf', C=1E6)# Radial Basis Function(RBF)
#model.fit(X, y)

def plot_svc_decision_function(model, ax=None, plot_support=True):
    """Plot the decision function for a 2D SVC"""
    if ax is None:
        ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    #create grid to evaluate model
    x = np.linspace(xlim[0], xlim[1], 30)
    y = np.linspace(ylim[0], ylim[1], 30)
    Y, X = np.meshgrid(y, x)
    xy = np.vstack([X.ravel(),Y.ravel()]).T
    P = model.decision_function(xy).reshape(X.shape)

    #plot decision boundary and margins
    ax.contour(X, Y, P, colors='k', levels=[-1, 0, 1], alpha=0.5,
                linestyles=['--', '-', '--'])

    #plot support vectors
    if plot_support:
        ax.scatter(model.support_vectors_[:,0],
                    model.support_vectors_[:,1],
                    s=300,linewidth=1,facecolors="none")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

#plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
plot_svc_decision_function(model,plot_support=False)

#plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1],
            #s=300, lw=1, facecolors='none')
plt.show()

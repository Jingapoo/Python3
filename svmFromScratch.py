import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from sklearn.svm import SVC #Support Vector Classifier
from sklearn.datasets.samples_generator import make_blobs

sns.set()

#generate random data X and y using sklearn make_blobs and plot it.
X,y =  make_blobs(n_samples=50,centers=2,cluster_std=0.60,random_state=0)
#plt.scatter(X[:, 0], X[:, 1], c=y,s=50,cmap="autumn")
#plt.show()
'''
# creating line space
xfit = np.linspace(-1,3.5)
plt.scatter(X[:, 0], X[:, 1], c=y,s=50,cmap="autumn")

# plot a line between the different sets of data
#Maximizing the Margin
for m, b, d in [(1, 0.65, 0.33), (0.5, 1.6, 0.55), (-0.2, 2.9, 0.2)]:
    yfit = m * xfit + b
    plt.plot(xfit, yfit, '-k')
    plt.fill_between(xfit, yfit - d, yfit + d, edgecolor='none', color='#AAAAAA', alpha=0.4)
plt.xlim(-1, 3.5)
plt.show()
'''

#Fitting a support vector machine
model = SVC(kernel='linear',C=1E10)
model.fit(X, y)

#plot SVM decision boundaries
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

plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
#plot_svc_decision_function(model)
plt.show()
#This is the dividing line that maximizes the margin between
#the two sets of points. Notice that a few of the training points just
#touch the margin, these points are the pivotal(关键的)elements of this fit,
#and are known as the support vectors
'''
#plot the model learned from the first 60 points and
#first 120 points of this dataset
def plot_svm(N=10, ax=None):
    X, y = make_blobs(n_samples=200, centers=2,
                      random_state=0, cluster_std=0.60)
    X = X[:N]
    y = y[:N]
    model = SVC(kernel='linear', C=1E10)
    model.fit(X, y)

    ax = ax or plt.gca()
    ax.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 6)
    plot_svc_decision_function(model, ax)

fig, ax = plt.subplots(1, 2, figsize=(16, 6))
fig.subplots_adjust(left=0.0625, right=0.95, wspace=0.1)
for axi, N in zip(ax, [60, 120]):
    plot_svm(N, axi)
    axi.set_title('N = {0}'.format(N))
plt.show()
#In the left panel, we see the model and the support vectors for 60 training
#points. In the right panel, we have doubled the number of training points,
#but the model has not changed: the three support vectors from the left panel
#are still the support vectors from the right panel. This insensitivity to the
#exact behavior of distant points is one of the strengths of the SVM model.
'''

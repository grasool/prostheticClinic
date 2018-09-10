#source of Example
#http://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2],[6,7],[8,7],[9,9]])
y = np.array([1, 1, 1, 2, 2, 2,3,3,3])

print(X)
print(X[0])
#adding third dimension to array
##X = np.array([[[-8,-7,-6],[-5,-4,-3],[-2,-1,0]],[[8,5,6],[7,3,4],[3,2,1]]])
##y = np.array([[1,1,1],[2,2,2]])

clf = LinearDiscriminantAnalysis()
clf.fit(X, y)

print(clf.predict([[6, 6],[-1,-2]]))
#print(clf.predict([[-8,-4,-3],[7,1,5]]))

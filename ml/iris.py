from sklearn.datasets import load_iris, load_boston, load_wine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, precision_score, plot_confusion_matrix
x,y = load_iris(return_X_y=True)

x_train, x_test, y_train , y_test = train_test_split(x,y, train_size=.8)
lr = LogisticRegression(max_iter=50, multi_class='ovr')
lr.fit(X=x_train, y=y_train)

res =lr.score(X=x_test, y=y_test)

y_pred = lr.predict(x_test)
print(precision_score(y_true=y_test, y_pred=y_pred, average=None))

print(res)

disp = plot_confusion_matrix(lr, x_test, y_test)
print(disp.confusion_matrix)

print(classification_report(y_true=y_test, y_pred = y_pred))

print('-'*16)
print('oaston')

wine_x,wine_y = load_wine(return_X_y=True)
wdf = load_wine()
wine_lr = LogisticRegression(max_iter=50)
print(wdf.DESCR)

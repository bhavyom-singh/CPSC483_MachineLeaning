import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

all_data = pd.read_csv("Data/emails.csv")
print("no. of rows in data = {}".format(len(all_data)))
X_train, X_test, Y_train, Y_test = train_test_split(all_data.text, all_data.spam, test_size = 0.25)

v = CountVectorizer()
X_train_count = v.fit_transform(X_train.values)
print(X_train_count.toarray()[:3])

#print(all_data.head())

model = KNeighborsClassifier(n_neighbors=3)

model.fit(X_train_count, Y_train)

X_test_count = v.transform(X_test)
print("KNN score : {}".format(model.score(X_test_count, Y_test)))

Y_pred = model.predict(X_test_count)

#Y_test_count = v.transform(Y_test.values)
confusion_matrix = confusion_matrix(Y_test, Y_pred)
print("Confusion matrix : {}".format(confusion_matrix))

TN = confusion_matrix[0,0]
TP = confusion_matrix[1,1]
FN = confusion_matrix[1,0]
FP = confusion_matrix[0,1]

print("TN : {}".format(TN))
print("TP : {}".format(TP))
print("FN : {}".format(FN))
print("FP : {}".format(FP))

print("Sensitivity : {}".format(TP/(TP+FN)))
print("Specificity : {}".format(TN/(TN+FP)))
print("Precision : {}".format(TP/(TP+FP)))

Y_pred_prob = model.predict_proba(X_test_count)[:,1]

fpr, tpr, thresholds = roc_curve(Y_test, Y_pred_prob)

error_H = (FN + FP)/(TN + TP + FN + FP)
confidence_plus = error_H + 1.96 * (np.sqrt(error_H * (1 - error_H) / (TN + TP + FN + FP)))
confidence_minus = error_H - 1.96 * (np.sqrt(error_H * (1 - error_H) / (TN + TP + FN + FP))) 
print("Confidence Level range from {} to {}".format(confidence_plus, confidence_minus))

plt.plot(fpr, tpr, label = 'ROC Curve')
plt.plot([0,1],[0,1], 'k--', label = 'Random guess')
_ = plt.xlabel('False Positive Rate')
_ = plt.ylabel('True Positive Rate')
_ = plt.title('ROC Curve')
# _ = plt.xlim([-0.02, 1])
# _ = plt.ylim([0, 1.02])
_ = plt.legend(loc = "lower right")
plt.show()
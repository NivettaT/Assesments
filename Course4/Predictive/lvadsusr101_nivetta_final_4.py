# -*- coding: utf-8 -*-
"""LVADSUSR101_Nivetta_Final_4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r2hxN3zhhaKnScEXQ1zUFGx7v_ZuVUoK
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, classification_report
import warnings as wr
wr.filterwarnings("ignore")

#reading data
data1 = pd.read_csv("/content/social_network.csv")
data1.head()

# duplicate check
dup_no = data1.duplicated().sum()
print('Total number of duplicated records: ', dup_no)
# drop duplicates if exist
data1 = data1.drop_duplicates()

# null check
data1.isnull().sum()
# if null is there, then impute with mean if normally distributed else with median

# outliers check
q1 = data1.quantile(0.25)
q3 = data1.quantile(0.75)
IQR = q3 - q1
threshold = 1.5
outliers = (data1 < (q1 - threshold * IQR)) | (data1 > (q3 + threshold * IQR))
data = data1[~outliers.any(axis=1)]
print('Number of outliers removed: ', len(data1) - len(data))

for i in data.drop(['user_id','account_creation_date'], axis = 1):
    plt.figure()
    sns.histplot(data[i], kde=True)
    plt.title(f'Histogram of {i}')
    plt.xlabel(i)
    plt.ylabel('Frequency')
    plt.show()

#Define features and target
X = data[['login_activity', 'posting_activity', 'social_connections']]
y = data['suspicious_activity']

#Spliting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = IsolationForest(contamination=0.1)
clf.fit(X_train)

y_pred = clf.predict(X_test)

y_pred = clf.predict(X_test)
y_pred[y_pred == 1] = 0
y_pred[y_pred == -1] = 1

features = ["login_activity", "posting_activity", "social_connections"]
X = data[features]
model = IsolationForest()
model.fit(X)
y_pred = model.predict(X)
data["anomaly_score"] = model.decision_function(X)
anomalies = data.loc[data["anomaly_score"] < 0]

df_test= pd.read_csv("/content/social_network.csv")
x=df_test[["login_activity", "posting_activity", "social_connections"]]
df_values=x.values

find=df_values

result=[]
for i in find:
  z=model.predict([i])
  if z==[1]:
    result.append('Not Anomaly')
  elif z==[-1]:
    result.append('Anomaly')

df_test['Anomaly']=result

plt.scatter(data["social_connections"], data["anomaly_score"], label="Not Anomaly")
plt.scatter(anomalies["social_connections"], anomalies["anomaly_score"], color="r", label="Anomaly")
plt.xlabel("Social Connections")
plt.ylabel("anomaly_score")
plt.legend()
plt.show()

#Evaluating the model
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))
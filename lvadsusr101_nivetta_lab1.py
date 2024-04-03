# -*- coding: utf-8 -*-
"""LVADSUSR101_Nivetta_Lab1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YtnCTjKyk16zru-n4JGYEOAZf3Ung6DF
"""

import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings as wr
wr.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# read data
data1 = pd.read_csv('/content/expenses.csv')
data1.info()
data1.describe()
data1.head(5)

# duplicate check
dup_no = data1.duplicated().sum()
print('Total number of duplicated records: ',dup_no)
# drop duplicates
data1 = data1.drop_duplicates()

# null check
data1.isnull().sum() # we can see that there are no null values present, hence no need to impute

# outliers check
q1 = data1.quantile(0.25)
q3 = data1.quantile(0.75)
IQR = q3-q1
threshold = 1.5
outliers = (data1 < (q1-threshold* IQR)) | (data1 > (q3+threshold* IQR))
data = data1[~outliers.any(axis=1)]
print('Number of outliers removed: ',len(data1)-len(data))

# Plot histograms for each feature
for i in data.columns:
    plt.figure()
    sns.histplot(data[i], kde=True)
    plt.title(f'Histogram of {i}')
    plt.xlabel(i)
    plt.ylabel('Frequency')
    plt.show()

# corr matrix
plt.figure(figsize=(8, 6))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()

# encoding categorical values (have used get dummies way)
data_encoded = pd.get_dummies(data, columns = ['sex','smoker','region'])
data_encoded.head()

# # drop unecessary fields
# data_cleaned = data_encoded.drop(['region'], axis=1)

# Splitting the Data into Train and Test Sets
X = data_encoded.drop(['charges'], axis=1)
y = data_encoded['charges']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Model development
model = LinearRegression()
model = model.fit(X_train,y_train)
pred = model.predict(X_test)

# Model Evaluation
r2 = r2_score(y_test,pred)
mse = mean_squared_error(y_test,pred,squared=False)
rmse = np.sqrt(mse)
print("The R2 score is: ",r2)
print("The mean squared error is: ",mse)
print("Rmse is: ", rmse)

"""The more the learning rate the more the convergence."""
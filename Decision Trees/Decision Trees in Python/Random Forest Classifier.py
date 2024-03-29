#!/usr/bin/env python
# coding: utf-8

# In[60]:


# importing necessary libraries
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


import matplotlib.pyplot as plt
import graphviz 
import seaborn as sns

import pandas as pd
import numpy as np

import warnings

# reading the data
df = pd.read_csv("decision_trees_data.csv")
print(df.head())

# converting to proper datatypes
df['origin_latitude'] = df['origin_latitude'].astype('category')
df['origin_longitude'] = df['origin_longitude'].astype('category')
df['destination_latitude'] = df['destination_latitude'].astype('category')
df['destination_longitude'] = df['destination_longitude'].astype('category')
df['total_weather_delay'] = df['total_weather_delay'].astype('category')

print(df.info())

# checking for class imbalance 
df['total_weather_delay'].value_counts().plot(kind='bar', color=['lightblue', 'darkblue'])
plt.xlabel('Categories')
plt.ylabel('Counts')
plt.title('Check for class imbalance')
plt.show()

#creating training and testing dataset
X = df.drop(columns=['total_weather_delay']) 
y = df['total_weather_delay']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,stratify=y)

# building the random forest classifier data model
model = RandomForestClassifier(n_estimators=100,criterion = 'entropy')
model.fit(X_train,y_train)

# creating confusion matrix
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test,y_pred)
print(cm)

#visualizing the heatmap for confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True, xticklabels=['Extended Delay','Short Delay'], yticklabels=['Extended Delay','Short Delay'])
plt.title('Confusion Matrix')
plt.xlabel('Actual')
plt.ylabel('Predicted')



plt.show()

# plotting feature importance bar
col = ['origin_latitude' ,'origin_longitude' ,'destination_latitude' ,'destination_longitude','origin_temperature','destination_temperature']
y = model.feature_importances_
fig, ax = plt.subplots() 
width = 0.4  
ind = np.arange(len(y))
ax.barh(ind, y, width, color="green")
ax.set_yticks(ind+width/10)
ax.set_yticklabels(col, minor=False)
plt.title('Feature importance in RandomForest Classifier')
plt.xlabel('Relative importance')
plt.ylabel('feature') 
plt.figure(figsize=(5,5))
fig.set_size_inches(6.5, 4.5, forward=True)


# visualizing the tree
tree_graph = tree.export_graphviz(model.estimators_[0], out_file=None,
                                  feature_names=X_train.columns,
                                  filled=True,
                                  rounded=True,
                                  special_characters=True)

graph = graphviz.Source(tree_graph)
graph.render("Tree_Record_Gini2")

# Display classification report
report = classification_report(y_test, y_pred)
print("Classification Report:")
print(report)


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing necessary libraries
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# In[2]:


data_kmeans = pd.read_csv("clustering_data.csv")

data_kmeans.head()

scaler = StandardScaler()
scaled = scaler.fit_transform(data_kmeans)
scaled = pd.DataFrame(scaled, columns=data_kmeans.columns)


# In[3]:


inertias = []
max_clusters = 10
for i in range(1,max_clusters):
    kmeans = KMeans(n_clusters=i,n_init='auto')
    kmeans.fit(scaled)
    inertias.append(kmeans.inertia_)

plt.plot(range(1,max_clusters), inertias, marker='o')
plt.title('Elbow method')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()



# In[4]:


silhouette_avg = []

for i in range(2, 10):
    # initialize kmeans
    kmeans = KMeans(n_clusters=i,n_init='auto')
    kmeans.fit(scaled)
    cluster_labels = kmeans.labels_

    # silhouette score
    silhouette_avg.append(silhouette_score(data_kmeans, cluster_labels))

# Plotting the results
plt.plot(range(2, 10), silhouette_avg, 'bx-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Analysis For Optimal K')
plt.show()


# In[5]:


kmeans_n3 = KMeans(n_clusters=3,random_state=123,n_init='auto')
kmeans_n3.fit(scaled)

My_labels3 = kmeans_n3.predict(scaled)
data_kmeans.loc[:, 'Cluster'] = My_labels3
sns.scatterplot(x = "origin_temperature", y ="origin_weather_delay",hue = "Cluster",data = data_kmeans)


# In[7]:


kmeans_n4 = KMeans(n_clusters=2,random_state=123, n_init='auto')
kmeans_n4.fit(scaled)

My_labels3 = kmeans_n4.predict(scaled)

data_kmeans.loc[:, 'Cluster'] = My_labels3
import seaborn as sns
sns.scatterplot(x = "origin_temperature", y ="origin_weather_delay",hue = "Cluster",data = data_kmeans)


# In[8]:


kmeans_n4 = KMeans(n_clusters=4,random_state=123, n_init='auto')
kmeans_n4.fit(scaled)

My_labels3 = kmeans_n4.predict(scaled)

data_kmeans.loc[:, 'Cluster'] = My_labels3
import seaborn as sns
sns.scatterplot(x = "origin_temperature", y ="origin_weather_delay",hue = "Cluster",data = data_kmeans)


# In[ ]:





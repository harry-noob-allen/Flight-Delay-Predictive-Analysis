# importing necessary libraries
library(lsa)
library(proxy)
library(ggplot2)

# reading the preprocessed data
data <- read.csv('clustering_data.csv')

head(data)

# scaling the data before applying cosine similarity
df_standardized <- scale(data)

# applying cosine similarity
cosine_similarity <- proxy::dist(df_standardized, method = "cosine")

# clustering using ward linkage
clustering_ward <- hclust(cosine_similarity, method = "ward.D")

# clustering using complete linkage
clustering_complete <- hclust(cosine_similarity, method = "complete")

# Visualize dendrogram for ward linkage
plot(clustering_ward, labels = FALSE)

# Visualize dendrogram for complete linkage
plot(clustering_complete, labels = FALSE)

# fitting the clusters based on complete linkage with number of clusters as 2
fit1 <- cutree(clustering_ward, k = 2)
table(fit1)

# fitting the clusters based on complete linkage with number of clusters as 3
fit2 <- cutree(clustering_ward, k = 3)
table(fit2)

# fitting the clusters based on complete linkage with number of clusters as 4
fit3 <- cutree(clustering_ward, k = 4)
table(fit3)

# adding the columns to the dataframe as factors 
data$cluster1 = as.factor(fit1)
data$cluster2 = as.factor(fit2)
data$cluster3 = as.factor(fit3)

# displaying the top data
head(data)

# setting the colors for the plot
cluster_colors <- c("1" = "#f03c3cf4", "2" = "#28ec28f7", "3" = "#5fa9e5" , "4" = "#D6B454")

# plotting scatter plot for origin temperature vs origin delay for clusters = 2
ggplot(data, aes(x = origin_temperature, y = origin_weather_delay, color = cluster1)) +
  geom_point() +
  scale_color_manual(values = cluster_colors)+
  theme_minimal() +
  labs(title = "Cluster Plot of Origin temperature vs Origin Weather Delay", x = "Origin Temperature", y = "Origin Delay")

# plotting scatter plot for origin temperature vs origin delay for clusters = 3
ggplot(data, aes(x = origin_temperature, y = origin_weather_delay, color = cluster2)) +
  geom_point() +
  scale_color_manual(values = cluster_colors)+
  theme_minimal() +
  labs(title = "Cluster Plot of Origin temperature vs Origin Weather Delay", x = "Origin Temperature", y = "Origin Delay")

# plotting scatter plot for origin temperature vs origin delay for clusters = 4
ggplot(data, aes(x = origin_temperature, y = origin_weather_delay, color = cluster3)) +
  geom_point() +
  scale_color_manual(values = cluster_colors)+
  theme_minimal() +
  labs(title = "Cluster Plot of Origin temperature vs Origin Weather Delay", x = "Origin Temperature", y = "Origin Delay")





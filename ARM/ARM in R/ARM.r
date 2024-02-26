# importing necessary libraries
library(viridis)
library(arules)
library(TSP)
library(data.table)
library(tcltk)
library(dplyr)
library(devtools)
library(purrr)
library(tidyr)
library(arulesViz)
library(RColorBrewer)
library(htmlwidgets)

# reading the pre-processed data as transactions
arm_origin <- read.transactions("arm_origin.csv",
                           rm.duplicates = FALSE, 
                           format = "basket", 
                           sep=",")

# displaying the transaction data
inspect(arm_origin)

# creating rules for delay(Case 1)
Frules_only_delay = arules::apriori(arm_origin, parameter = list(support=.05, 
                                          confidence=.05, minlen=2),
                        appearance = list(default="lhs", rhs="Delay"))
# Displaying the rules
inspect(Frules_only_delay)

print("-----------------------------------------------------------------------")
print ("                                                                      ")
print("Top 15 rules by support")
print ("                                                                      ")
print("-----------------------------------------------------------------------")

# Sorting the top 15 rules by support
SortedRulesOnlyDelay <- sort(Frules_only_delay, by="support", decreasing=TRUE)

# Displaying the rules
inspect(SortedRulesOnlyDelay[1:15])


print("-----------------------------------------------------------------------")
print ("                                                                      ")
print("Top 15 rules by Confidence")
print ("                                                                      ")
print("-----------------------------------------------------------------------")

# Sorting the top 15 rules by confidence
SortedRulesOnlyDelay_Confidence <- sort(Frules_only_delay, by="confidence", decreasing=TRUE)

# Displaying the rules
inspect(SortedRulesOnlyDelay_Confidence[1:15])
print ("                                                                      ")
print("Top 15 rules by lift")
print ("                                                                      ")
print("-----------------------------------------------------------------------")

# Sorting the top 15 rules by lift
SortedRulesOnlyDelay_Lift <- sort(Frules_only_delay, by="lift", decreasing=TRUE)

# Displaying the rules
inspect(SortedRulesOnlyDelay_Lift[1:15])


# creating rules for delay and all factors (Case 2)
Frules_delay = arules::apriori(arm_origin, parameter = list(support=.007, 
                                          confidence=.05, minlen=4),
                        appearance = list(default="lhs", rhs="Delay"))

# Displaying the rules
inspect(Frules_delay)

print("-----------------------------------------------------------------------")
print ("                                                                      ")
print("Top 15 rules by support")
print ("                                                                      ")
print("-----------------------------------------------------------------------")

# Sorting the top 15 rules by support
SortedRules_Support <- sort(Frules_delay, by="support", decreasing=TRUE)

# Displaying the rules
inspect(SortedRules_Support[1:15])

print ("                                                                      ")
print("Top 15 rules by confidence")
print ("                                                                      ")
print("-----------------------------------------------------------------------")

# Sorting the top 15 rules by confidence
SortedRules_Confidence <- sort(Frules_delay, by="confidence", decreasing=TRUE)

# Displaying the rules
inspect(SortedRules_Confidence[1:15])

print ("                                                                      ")
print("Top 15 rules by lift")
print ("                                                                      ")
print("-----------------------------------------------------------------------")

# Sorting the top 15 rules by lift
SortedRules_Lift <- sort(Frules_delay, by="lift", decreasing=TRUE)
# Displaying the rules
inspect(SortedRules_Lift[1:15])




print ("                                                                      ")
print("Network Graph for case 1")
print ("                                                                      ")
print("-----------------------------------------------------------------------")

# plotting the rules of case 2 using network graph
subrulesOnlyDelay <- head(sort(SortedRulesOnlyDelay, by="lift"),15)
subrulesOnlyDelayplot <- plot(subrulesOnlyDelay, method="graph", engine="htmlwidget")
subrulesOnlyDelayplot


print ("                                                                      ")
print("Network Graph for case 2")
print ("                                                                      ")
print("-----------------------------------------------------------------------")

# plotting the rules of case 2 using network graph
a <- plot(subrulesK, method="graph", engine="htmlwidget")

# saving the graph in local
saveWidget(a, file = "case2.html",selfcontained = FALSE)

a



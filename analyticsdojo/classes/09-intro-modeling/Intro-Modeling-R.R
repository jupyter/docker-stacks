

#The Iris Data 
#http://cran.r-project.org/doc/contrib/Zhao_R_and_data_mining.pdf 
#See Section 1.3
#The data is included with R, so we just have to call it. 
#This is a traditional "Classification" Problem
library(ggplot2)
iris<-iris
summary (iris)
str(iris)
hist(iris$Sepal.Length)
plot(density(iris$Sepal.Length))
pie(table(iris$Species))

#Basic Correlation 
cor(iris[,1:4])
#Aggregate Data 
aggregate(Sepal.Length ~ Species, summary, data=iris)
boxplot(Sepal.Length~Species, data=iris)
install.packages("scatterplot3d")
library(scatterplot3d)
scatterplot3d(iris$Petal.Width, iris$Sepal.Length, iris$Sepal.Width)

library(MASS)
parcoord(iris[1:4], col=iris$Species)
install.packages("ggplot2")

library(ggplot2)
qplot(Sepal.Length, Sepal.Width, data=iris, facets=Species ~.)

#1. Desribe what you find through visualizing the data. What intuition 
#would a classifier have to capture to categorize the data?

#This pulls out 70% for training data.
#This starts on P. 29 of http://cran.r-project.org/doc/contrib/Zhao_R_and_data_mining.pdf 

#This creates a vector indicator we will use to 
#select our training and test dataset 
set.seed(1234)
ind <- sample(2, nrow(iris), replace=TRUE, prob=c(0.7, 0.3))

#Select our training data
trainData <- iris[ind==1,]

#Select our test data
testData <- iris[ind==2,]
#This is a package that includes a decision Tree 
install.packages('party')
library(party)

#This specifies the formula
myFormula <- Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width
#This generates the decision tree
iris_ctree <- ctree(myFormula, data=trainData)


#This creats a new variable 
trainData$pred_ctree<-predict(iris_ctree)
plot(iris_ctree)

table(trainData$pred_ctree, trainData$Species)
trainData$correct<-ifelse(trainData$pred_ctree==trainData$Species, 1, 0)

#This shows the percentage of the data correctly predicted.
summary(trainData$correct)

#2 Which class was most likely to be misclassified?  How many total were misclassified?

#3 Explain the logic found in the first node of the decision tree.

#4 Rerun the analysis using only 20% of the data as a training.  What % is correct?

plot(iris_ctree, type="simple")
testData$pred_ctree <- predict(iris_ctree, newdata = testData)
testData$correct<-ifelse(testData$pred_ctree==testData$Species, 1, 0)

#5 What % of the predictions are correct in the test data?

#6 Would you expect the % classified correctly to be higher
#in the training or test analysis?


install.packages('randomForest')
library('randomForest')
rf <- randomForest(Species ~ ., data=trainData, ntree=100, proximity=TRUE)
trainData$pred_rf<-predict(rf)
table(trainData$pred_rf, trainData$Species)
print(rf) 
plot(rf)
importance(rf)


#7 Calculate the % classified corectly in the random forest prediction 
# for both the training and the test set.  

#8 What does "importance" tell us?










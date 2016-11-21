#Set the appropriate working directory. 
setwd("~/githubdesktop/materials/analyticsdojo/data")
boston <- read.csv("boston.csv", stringsAsFactors=FALSE)
#Let's keep the same nameing as in Python.
y<-boston$PRICE
X<-boston[,2:14]

#But now recombine to one dataframe.
boston2<-cbind(y,X)
#This trains the model
lmresults<-lm(y~., data=boston2)
#this ouputs the result. 
summary(lmresults)

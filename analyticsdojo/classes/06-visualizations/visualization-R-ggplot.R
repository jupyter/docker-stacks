#IRIS Plots

#This is a basic visualization. 

#Set your working directory. For example:
# setwd("~/githubdesktop/materials/analyticsdojo/classes/06-visualizations")
iris<-read.csv(file="../../data/iris.csv", header=TRUE,sep=",")


#Exploratory
pairs(iris[1:4], main = "Iris Data", pch = 21, bg = c("red", "green3", "blue")[unclass(iris$species)])

hist(iris$petalWidth)
hist(iris$sepalLength)
hist(iris$sepalWidth)

iris.setosa<-iris[iris$species=="setosa",]
iris.versicolor<-iris[iris$species=="versicolor",]
iris.virginica<-iris[iris$species=="virginica",]

#Here we can check to see if some of issues with histogram 
#Were based upon different species.
hist(iris.versicolor$petalWidth)
hist(iris.setosa$petalWidth)
hist(iris.virginica$petalWidth)

#Simple Basic Plot
plot(iris$petalLength, iris$petalWidth, main="Iris Data")

#Complex Plot
plot(iris$petalLength, iris$petalWidth, pch=21, bg=c("red","green3","blue")[unclass(iris$species)], main="Edgar Anderson's Iris Data")

#Make it look cooler with ggplot.
install.packages("ggplot2")
library(ggplot2)

ggplot(data=iris, aes(x=sepalLength, y=sepalWidth, color=species)) + geom_point(size=3)

#BoxPlot
ggplot(iris, aes(x=species,y=sepalLength)) + geom_boxplot()

#Histogram
ggplot(iris, aes(sepalLength)) + geom_histogram ()

install.packages("GGally", repos="http://cran.us.r-project.org")
#For a more detailed version, see http://tutorials.iq.harvard.edu/R/Rgraphics/Rgraphics.html
#GGally is an extension to ggplot that enables pairwise. 
library(GGally)
ggpairs(iris, mapping = aes(color = species))

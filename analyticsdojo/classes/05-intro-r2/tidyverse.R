
#Tidyverse Demo
setwd("~/githubdesktop/materials/analyticsdojo/classes/05-intro-r2")
install.packages("tidyverse")
install.packages("nycflights13")
library(nycflights13)
library(tidyverse)
#Piping Demo
#This just gives a dataframe with 234 obs 
mpg<-mpg

#This just gives a dataframe with 70 obs, only 8 cylinder cars 
mpg.8cyl<-mpg %>% 
  filter(cyl == 8)

#This takes the mean city MPG by manufacturer 
mpg.8cyl %>% #This starts with are saved dataframe.
  group_by(manufacturer) %>% 
  summarise(citympg = mean(cty))

## DPLYR
#Filter to only those cars that have miles per gallon equal to 
mpg.8cyl<-mpg %>% 
  filter(cyl == 8)

#Alt Syntax
mpg.8cyl<-filter(mpg, cyl == 8)

#Flights on the 1/1
flight11<-filter(flights, month == 1, day == 1) 


#Select Example 
Petal<-select(iris, starts_with("Petal"))
select(iris, ends_with("Width"))
select(iris, contains("etal"))
select(iris, matches(".t."))
select(iris, Petal.Length, Petal.Width)
vars <- c("Petal.Length", "Petal.Width")
select(iris, one_of(vars))

# This sorts the data
mpgsort<-arrange(mpg, hwy, cty)

#recode
mpg<-mpg
mpg2<-mutate(mpg, displ_l = displ / 61.0237)

mpg %>%
  mutate(mpg, displ_l = displ / 61.0237) 


section <- c("MATH111", "MATH111", "ENG111")
grade <- c(78, 93, 56)
student <- c("David", "Kristina", "Mycroft")
gradebook <- data.frame(section, grade, student)

gradebook2<-mutate(gradebook, Pass.Fail = ifelse(grade > 60, "Pass", "Fail"))  
gradebook3<-mutate(gradebook2, letter = ifelse(grade %in% 60:69, "D",
                                               ifelse(grade %in% 70:79, "C",
                                                      ifelse(grade %in% 80:89, "B",
                                                             ifelse(grade %in% 90:99, "A", "F")))))


gradebook4<-gradebook %>%
  mutate(Pass.Fail = ifelse(grade > 60, "Pass", "Fail"))  %>%
  mutate(letter = ifelse(grade %in% 60:69, "D", 
                         ifelse(grade %in% 70:79, "C",
                                ifelse(grade %in% 80:89, "B",
                                       ifelse(grade %in% 90:99, "A", "F")))))

#find the average city and highway mpg
summarise(mpg, mean(cty), mean(hwy))
#find the average city and highway mpg by cylander
summarise(group_by(mpg, cyl), mean(cty), mean(hwy))
summarise(group_by(mtcars, cyl), m = mean(disp), sd = sd(disp))

# With data frames, you can create and immediately use summaries
by_cyl <- mtcars %>% group_by(cyl)
by_cyl %>% summarise(a = n(), b = a + 1)

#Tibble Demo
iris<-as_tibble(read.csv(file="../../data/iris.csv", header=TRUE,sep=","))
#you can see this is of class tbl_df
class(iris)
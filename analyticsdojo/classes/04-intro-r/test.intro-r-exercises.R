
context("Homework 4")
  
  test_that("Q1 Create a variable called sepalWidth.mean", {
    expect_equal(sepalWidth.mean, 3.054)
  })
  
  test_that("Q2Create a new column of iris.df called sepalArea", {
    expect_equal(mean(iris.df$sepalArea), 17.80653,tolerance=1e-3)
  })
  
  test_that("Q3 Create a new dataframe iristrain.df that includes the first 75 rows", {
    expect_equal(nrow(iristrain.df), 75)
    expect_equal(mean(iristrain.df$sepalLength), 5.341333,tolerance=1e-3)
  })
  
  test_that("Q4 Create a new dataframe iristest.df that includes the last 75 rows of the iris dataframe.", {
    expect_equal(nrow(iristest.df), 75)
    expect_equal(mean(iristest.df$sepalLength), 6.345333,tolerance=1e-3)
  })
  
  test_that("(5). Create a new vector sepalLength from the sepalLength column of the iris dataframe.", {
    expect_equal(mean(sepalLength), 5.843333,tolerance=1e-3)
    expect_equal(length(sepalLength), 150)
  })
  
  test_that("(5). Create a new vector sepalLength from the sepalLength column of the iris dataframe.", {
    expect_equal(mean(sepalLength), 5.843333,tolerance=1e-3)
    expect_equal(length(sepalLength), 150)
  })
  
  test_that("(6). AccEveryoneDies and AccGender", {
    expect_equal(AccEveryoneDies, 61.61616,tolerance=1e-3)
    expect_equal(AccGender, 78.6756453423,tolerance=1e-3)
    expect_equal( mean(train$PredGender), 0.352413,tolerance=1e-3)
    expect_equal( sum(train$PredEveryoneDies), 0)
  })
  
  test_that("(8). PredGenderAge13 and PredGenderAge18", {
    expect_equal(AccGenderAge13, 79.2368125701,tolerance=1e-3)
    expect_equal(AccGenderAge18, 77.3288439955,tolerance=1e-3)
    expect_equal( mean(train$PredGenderAge13), 0.393939393939,tolerance=1e-3)
    expect_equal( mean(train$PredGenderAge18), 0.417508417508, tolerance=1e-3)
  })
  
  test_that("(9). Child", {
    expect_equal(sum(train$child), 69)
    expect_equal(sum(test$child), 25)
     })

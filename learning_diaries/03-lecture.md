---
title: "Lecture 2"
date: "March 2020"
author: "Jalmari Tuominen"
---

Today's lecture was a recording from 2019 kept by a different teacher. We covered modelling with Logistics Regression for the first time which was interesting and worthwile.

I have just recently started digging into general linear regression (GLM) in my own work and the process has been both painstakingly difficult and interesting. In my opinion there are several challenges in using GLM in modelling.

Python has two libraries that provide GLM funcionality: statsmodels and scikit-learn. Statsmodels takes a more statistically oriented approach (as the name tells) providing p-values and an R-like summary table. This is a well established way to perform GLM in medical context and I suppose is the tool of choice when adjusting for certain variables and making inference.  

The GLM implementation of Scikit-learn is built with predictions in mind. It works extremely well with other components of sklearn which allows quick prototyping and cross-validation. On the other hand sklearn doesn't offer p-values which makes it hard to perform inference and communicate the results to a more statistically oriented collaborator.

Both of these libraries have a shared weakness: they don't provide a conventinent and customisable timeseries crossvalidation (TSCV). I am currently working with a timeseries prediction problem and it is surprising that TSCV is not provided as elegantly abstracted as all the other cross validation methods are. For example, when doing k-folds cross validation, one can write:

```Python
#https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html
from sklearn import datasets, linear_model
from sklearn.model_selection import cross_val_score
diabetes = datasets.load_diabetes()
X = diabetes.data[:150]
y = diabetes.target[:150]
lasso = linear_model.Lasso()
print(cross_val_score(lasso, X, y, cv=3))
```

Scikit-learn does have a [TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html) iterator but it does not integrate with `cross_val_*` methods. To me this is surprising and begs the question: have I understood the concept of TSCV thoroughly? Am I hoping for functionality that is unecessary? How other people have solved this?

I believe that testing a predictor in a situation where features and target variables have temporal dependance should be as easy as this:

```Python
from sklearn import datasets, linear_model
from sklearn.model_selection import cross_val_score, time_series_split

ts_data = datasets.load_timeseries()

X = ts_data.data[:150]
y = ts_data.target[:150]

tscv = time_series_split(horizon=1, window=20, initial_n_train=.5)

lasso = linear_model.LinearRegression()
results = cross_val_score(lasso, X, y, cv=tscv)

print(results.summary())

>>> | MAPE | MAE | RMSE |
    |------|-----|------|
    | 12   | 5   | 3.2  |
```

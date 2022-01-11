"""CSC110 final project, main module

Descriptions
===============================

This module contains the function we used to implement the
simple multiple regression model.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. All rights reserved.

This file is Copyright (c) 2020 Runshi Yang, Chenxu Wang and Haojun Qiu
"""
from typing import Dict
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np


def multiple_linear_regression(data: Dict,
                               temp: float,
                               prec: float) -> None:
    """Build a multiple linear regression model generated by the given data
    """
    keys = list(data.keys())
    df = pd.DataFrame(data, columns=[keys[0], keys[1], keys[2]])

    x1 = df[[keys[0], keys[1]]]
    y1 = df[keys[2]]

    # with sklearn
    regr = linear_model.LinearRegression()
    regr.fit(x1, y1)

    r_squared = 1 - (float(sum((y1 - regr.predict(x1)) ** 2))) / sum((y1 - np.mean(y1)) ** 2)
    adjusted_r_squared = 1 - (1 - r_squared) * (len(y1) - 1) / (len(y1) - x1.shape[1] - 1)

    print('r_squared: \n', r_squared)
    print('adjusted_r_squared: \n', adjusted_r_squared)
    print('Intercept: \n', regr.intercept_)
    print('Coefficients: \n', regr.coef_)

    ax = plt.figure().add_subplot(111, projection='3d')
    ax.scatter(df['temperature'], df['precipitation'], df['disease'], c='skyblue', s=60)
    ax.view_init(30, 185)
    plt.xlabel(keys[0])
    plt.ylabel(keys[1])

    x = np.arange(20, 80, 1.2)
    y = np.arange(2.5, 8.5, 0.12)
    z = regr.coef_[0] * x + regr.coef_[1] * y + regr.intercept_
    ax.plot3D(x, y, z, "gray")
    plt.show()

    # prediction with sklearn
    print('Predicted number of lyme cases: \n', regr.predict([[temp, prec]]))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pandas', 'sklearn', 'datetime', 'matplotlib.pyplot',
                          'numpy', 'python_ta'],
        'allowed-io': ['multiple_linear_regression'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
"""CSC110 final project, main module

Descriptions
===============================

This module contains all the functions we used to implement the
simple linear regression model.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. All rights reserved.

This file is Copyright (c) 2020 Runshi Yang, Chenxu Wang and Haojun Qiu
"""
from typing import List, Tuple
import plotly.graph_objects as go


def evaluate_line(a: float, b: float, x: float) -> float:
    """Evaluate the linear function y = a + bx for the given a, b.

    >>> result = evaluate_line(5.0, 1.0, 10.0)  # y = 5.0 + 1.0 * 10.0,
    >>> result == 15
    True
    """
    return a + b * x


def convert_points(points: List[tuple]) -> tuple:
    """Return a tuple of two lists, containing the x- and y-coordinates of the given points.

    >>> result = convert_points([(0.0, 1.1), (2.2, 3.3), (4.4, 5.5)])
    >>> result[0]  # The x-coordinates
    [0.0, 2.2, 4.4]
    >>> result[1]  # The y-coordinates
    [1.1, 3.3, 5.5]
    """
    x_coordinates = [x[0] for x in points]
    y_coordinates = [x[1] for x in points]
    return (x_coordinates, y_coordinates)


def simple_linear_regression(points: List[tuple]) -> tuple:
    """Perform a linear regression on the given points.

    This function returns a pair of floats (a, b) such that the line
    y = a + bx is the approximation of this data.

    Further reading: https://en.wikipedia.org/wiki/Simple_linear_regression

    Preconditions:
        - len(points) > 0

    >>> simple_linear_regression([(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)])
    (0.0, 1.0)
    """
    avg_x = sum(convert_points(points)[0]) / len(points)
    avg_y = sum(convert_points(points)[1]) / len(points)
    numerator = [(p[0] - avg_x) * (p[1] - avg_y) for p in points]
    denominator = [(p[0] - avg_x) ** 2 for p in points]
    b = sum(numerator) / sum(denominator)
    a = avg_y - b * avg_x
    return (a, b)


def calculate_r_squared(points: List[tuple], a: float, b: float) -> float:
    """Return the R squared value when the given points are modelled as the line y = a + bx.

    points is a list of pairs of numbers: [(x_1, y_1), (x_2, y_2), ...]

    Preconditions:
        - len(points) > 0
    """
    avg_y = sum(convert_points(points)[1]) / len(points)
    tot = [(avg_y - p[1]) ** 2 for p in points]
    res = [(p[1] - (a + b * p[0])) ** 2 for p in points]
    return 1 - sum(res) / sum(tot)


def perform_regression(train_data: List[tuple], xlabel: str,
                       title: str) -> Tuple[float, float, float]:
    """Return (a, b, r_squared)
    Plot all data points and regression line
    """
    # Get data points.
    points = train_data

    # Converts the points into the format expected by plotly.
    separated_coordinates = convert_points(points)
    x_coords = separated_coordinates[0]
    y_coords = separated_coordinates[1]

    # Do a simple linear regression. Returns the (a, b) constants for
    # the line y = a + b * x.
    model = simple_linear_regression(points)
    a = model[0]
    b = model[1]

    # Plot all the data points AND a line based on the regression
    plot_points_and_regression(x_coords, y_coords, [a, b], xlabel, title)

    # Calculate the r_squared value
    r_squared = calculate_r_squared(points, a, b)

    return (a, b, r_squared)


def plot_points_and_regression(x_coords: list, y_coords: list, coef: List[float],
                               xlabel: str, title: str) -> None:
    """Plot the given x- and y-coordinates and linear regression model using plotly.
    """
    # Create a blank figure
    layout = go.Layout(title=title,
                       xaxis={'title': xlabel},
                       yaxis={'title': 'number of cases'})

    fig = go.Figure(layout=layout)

    # Add the raw data
    fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='markers', name='Data'))

    # Add the regression line
    x_max = 1.1 * max(x_coords)
    fig.add_trace(go.Scatter(x=[0, x_max], y=[evaluate_line(coef[0], coef[1], 0),
                                              evaluate_line(coef[0], coef[1], x_max)],
                             mode='lines', name='Regression line'))

    # Display the figure in a web browser
    fig.show()


def predict(test_data: List[Tuple], model: Tuple[float, float, float],
            xlabel: str, title: str) -> float:
    """Return r_squared for the prediction.
    Plot all data points and regression line
    """
    # Get data points.
    points = test_data
    a = model[0]
    b = model[1]

    # Converts the points into the format expected by plotly.
    separated_coordinates = convert_points(points)
    x_coords = separated_coordinates[0]
    y_hat = separated_coordinates[1]

    # Plot all the data points AND a line based on the regression
    plot_points_and_regression(x_coords, y_hat, [a, b], xlabel, title)

    # Calculate the r_squared value
    r_squared = calculate_r_squared(points, a, b)

    return r_squared


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['plotly.graph_objects', 'python_ta'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

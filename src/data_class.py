"""CSC110 final project, main module

Descriptions
===============================

This module contains the data classes needed for the purpose of
storing data with natural meaning and in a more organized way.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. All rights reserved.

This file is Copyright (c) 2020 Runshi Yang, Chenxu Wang and Haojun Qiu
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Disease:
    """A custom datatype storing information about a type of disease in a region.

    Instance Attributes:
      - disease_name: the name of the disease type
      - monthly_cases: the newly occurred cases, stored by month

    Representation Invariants:
      - all(1 <= month <= 12 for month in self.monthly_cases)
      - all(0 <= self.monthly_cases[month] for month in self.monthly_cases)

    >>> lyme = Disease('lyme', [10.0, 20.0, 30.0])
    """
    disease_name: str
    monthly_cases: List[float]


@dataclass
class Climate:
    """A custom datatype storing information about monthly climate of a region.

    Instance Attributes:
      - mean_monthly_temp: the monthly average temperature
      - mean_monthly_precipitation: the monthly average precipitation

    Representation Invariants:
      - all(1 <= month <= 12 for month in self.monthly_temperature)
      - all(1 <= month <= 12 for month in self.monthly_precipitation)

    >>> climate2014 = Climate([50.0, 60.0], [2.5, 3.0])
    """
    monthly_mean_temperature: List[float]
    monthly_sum_precipitation: List[float]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['dataclasses', 'python_ta'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

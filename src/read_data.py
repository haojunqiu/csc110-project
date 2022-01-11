"""CSC110 final project, main module

Descriptions
===============================

This module is used to read data from csv files and transform them
into the correct form as the inputs for our regression functions.

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. All rights reserved.

This file is Copyright (c) 2020 Runshi Yang, Chenxu Wang and Haojun Qiu
"""
import datetime
import csv
from typing import Dict, List, Tuple
from data_class import Climate, Disease


###################################################################################################
# Functions that transform data to the input for linear regressions
###################################################################################################

def temp_disease_list_2016(filepath1: str, filepath2: str) -> List[Tuple[float, float]]:
    """Return the list of tuple, each tuple stores the mean temperature
    and disease cases in that month"""
    climate = extract_and_store_climate_data(filepath1)
    temperature_list = climate.monthly_mean_temperature
    disease = extract_and_store_disease_data(filepath2)
    disease_list = disease.monthly_cases

    list_so_far = []
    for i in range(12):
        list_so_far.append((temperature_list[i], disease_list[i]))

    return list_so_far


def prec_disease_list_2016(filepath1: str, filepath2: str) -> List[Tuple[float, float]]:
    """Return the list of tuple, each tuple stores the mean temperature
    and disease cases in that month"""
    climate = extract_and_store_climate_data(filepath1)
    precipitation_list = climate.monthly_sum_precipitation
    disease = extract_and_store_disease_data(filepath2)
    disease_list = disease.monthly_cases

    list_so_far = []
    for i in range(12):
        list_so_far.append((precipitation_list[i], disease_list[i]))

    return list_so_far


def temp_disease_list_2014(filepath1: str, filepath2: str) -> List[Tuple[float, float]]:
    """Return the list of tuple, each tuple stores the mean temperature
    and disease cases in that month"""
    with open(filepath1) as file:
        reader = csv.reader(file)

        next(reader)
        temperature_list = []
        disease = extract_and_store_disease_data(filepath2)
        disease_list = disease.monthly_cases
        for row in reader:
            list.append(temperature_list, float(row[1]))
        list_so_far = []
        for i in range(12):
            list_so_far.append((temperature_list[i], disease_list[i]))
        return list_so_far


def prec_disease_list_2014(filepath1: str, filepath2: str) -> List[Tuple[float, float]]:
    """Return the list of tuple, each tuple stores the precipitation
    and disease cases in that month"""
    with open(filepath1) as file:
        reader = csv.reader(file)

        next(reader)
        temperature_list = []
        disease = extract_and_store_disease_data(filepath2)
        disease_list = disease.monthly_cases
        for row in reader:
            list.append(temperature_list, float(row[2]))
        list_so_far = []
        for i in range(12):
            list_so_far.append((temperature_list[i], disease_list[i]))
        return list_so_far


def multiple_2014_data(filepath1: str, filepath2: str) -> Dict[str, List[float]]:
    """Return the dictionary of list, each list stores the precipitation,
        temperature, and disease cases in each month in 2014"""
    temp_disease_list = temp_disease_list_2014(filepath1, filepath2)
    prec_disease_list = prec_disease_list_2014(filepath1, filepath2)
    dic_so_far = {'temperature': [], 'precipitation': [], 'disease': []}
    for i in range(12):
        dic_so_far['temperature'].append(temp_disease_list[i][0])
        dic_so_far['precipitation'].append((prec_disease_list[i][0]))
        dic_so_far['disease'].append(temp_disease_list[i][1])

    return dic_so_far


###################################################################################################
# Functions that read and extract data from csv files, and that store them in our custom datatype
###################################################################################################


def extract_and_store_climate_data(filepath: str) -> Climate:
    """Extract United States climate data from the given filepath and transform it
    into Climate datatype.

        Preconditions:
            - filepath refers to a csv file in the format of
              datasets/weather_data_2016.csv
        """
    with open(filepath) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        # Set accumulators that store key value pairs, where key represents date,
        # and the corresponding value represent temperature or precipitation in that date
        daily_temperature = {}
        daily_precipitation = {}

        for row in reader:
            date = str_to_date(row[0])

            # 1. Extract temperature from raw data
            daily_temperature[date] = float(row[3])

            # 2. Extract precipitation from raw data
            if row[-3] == 'T':
                daily_precipitation[date] = 0.0
            else:  # when row[-3] != 0
                daily_precipitation[date] = float(row[-3])

        monthly_temps = convert_daily_temp_or_prec(daily_temperature)  # Group daily temp by month
        monthly_precs = convert_daily_temp_or_prec(daily_precipitation)  # Group daily prec by month

        # Calculate monthly mean temperature, storing into a list
        monthly_mean_temps = []
        for monthly_temp in monthly_temps:
            mean_temp_this_month = sum(monthly_temp) / len(monthly_temp)
            list.append(monthly_mean_temps, mean_temp_this_month)

        # Calculate monthly sum precipitation, storing into a list
        monthly_sum_precs = [sum(monthly_prec) for monthly_prec in monthly_precs]

        # Store two "monthly lists" into an empty Climate(our custom dataclass),
        # and we are done with our extraction!
        climate_data = Climate(monthly_sum_precipitation=monthly_sum_precs,
                               monthly_mean_temperature=monthly_mean_temps)

        return climate_data


def extract_and_store_disease_data(filepath: str) -> Disease:
    """Read the disease data from the given filepath and transform into a list of
    monthly disease cases

        Preconditions:
            - filepath refers to a csv file in the format of
              datasets/disease_2016.csv
        """
    # Transform weekly cases into daily cases, and group them in month.
    disease_daily = convert_csv_disease_data(filepath)
    cases_in_month = convert_disease(apply_date_time(disease_daily))

    # Set accumulator, for storing sum of cases in month
    monthly_disease_data = []

    # Sum up newly cases of each month, and store into a list
    for cases in cases_in_month:
        disease_this_month = sum(cases)
        list.append(monthly_disease_data, disease_this_month)

    # Store the cases list into out custom datatype —— Disease
    disease_data = Disease(disease_name='lyme', monthly_cases=monthly_disease_data)
    return disease_data


def str_to_date(date_string: str) -> datetime.date:
    """Convert a string in day-month-year format to a datetime.date.

    Preconditions:
    - date_string has format day-month-year

    >>> str_to_date('1-1-2016')
    datetime.date(2016, 1, 1)
    """
    time = str.split(date_string, '-')
    return datetime.date(int(time[2]), int(time[1]), int(time[0]))


def convert_csv_disease_data(filepath: str) -> List[float]:
    """read the weekly lyme disease data from the given filepath and transform into a list of
       the number of daily disease cases
       (we will assume the cases to be float to ensure its accuracy).


            Preconditions:
                - filepath refers to a csv file in the format of
                    datasets/disease_2016.csv
    """
    with open(filepath) as file:
        reader = csv.reader(file)

        next(reader)
        disease_so_far = []

        for row in reader:
            for _ in range(0, 7):
                list.append(disease_so_far, int(row[3]) / 7)
        return disease_so_far


def apply_date_time(disease_data: List[float]) -> Dict[datetime.date, float]:
    """ apply the datetime value for the daily disease_data in 2016(assume you already have weather
    data installed and have file path 'datasets/weather_data_nyc_centralpark_2016.csv')

    """
    with open('datasets/weather_2016.csv') as file:
        reader = csv.reader(file)

        next(reader)
        date_so_far = []
        dict_so_far = {}
        for row in reader:
            list.append(date_so_far, str_to_date(row[0]))
        for i in range(0, len(disease_data)):
            dict_so_far[date_so_far[i]] = disease_data[i]

        return dict_so_far


def convert_daily_temp_or_prec(daily_temperature: Dict[datetime.date, float]) -> List[list]:
    """convert the given dictionary of daily temperature into lists of temperature
    separated by month.

    """
    month_temp_so_far = []
    for i in range(1, 13):
        temp_this_month = []
        for date in daily_temperature:
            if date.month == i:
                list.append(temp_this_month, daily_temperature[date])
        list.append(month_temp_so_far, temp_this_month)
    return month_temp_so_far


def convert_disease(daily_disease: Dict[datetime.date, float]) -> List[list]:
    """Convert the given dictionary of weekly disease cases into lists containing
    lists each represents the monthly added cases

    """
    month_disease_so_far = []
    for i in range(1, 13):
        disease_this_month = []
        for date in daily_disease:
            if date.month == i:
                list.append(disease_this_month, daily_disease[date])
        list.append(month_disease_so_far, disease_this_month)
    return month_disease_so_far


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'datetime', 'typing', 'python_ta', 'data_class'],
        'allowed-io': ['temp_disease_list_2014', 'temp_disease_list_2016', 'prec_disease_list_2014',
                       'prec_disease_list_2016', 'multiple_2014_data', 'apply_date_time',
                       'convert_csv_disease_data', 'extract_and_store_climate_data'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

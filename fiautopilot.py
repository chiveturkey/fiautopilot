#!/usr/bin/python3

from math import log
import matplotlib.pyplot as plot
from matplotlib import rcParams
import numpy
import sqlite3
import os
import sys
import json


# Global Settings.

rcParams.update({'figure.autolayout': True})


# Constants

CONFIG_FILE = 'generalconfig.json'
PRINCIPAL_STOCK_HISTORY_FILE = 'principalstockhistory.json'
# These (apparently) magic numbers were arrived at by manually trying different values and then
# relating them to the ranges for x and y.
# TODO: Change names to Y_TEXT_SCALING_FACTOR_POSITION1 and Y_TEXT_SCALING_FACTOR_POSITION2, so
# they can be used more generally.
X_TEXT_SCALING_FACTOR = 4.41852918928
Y_TEXT_SCALING_FACTOR_YEARS = 33.958355966
Y_TEXT_SCALING_FACTOR_DOLLARS = 203.7501358

# If CONFIG_FILE exists, then use configuration values found there.  Otherwise,
# print an error.

if os.path.isfile(CONFIG_FILE):
    try:
        with open(CONFIG_FILE) as f:
            config_data = json.load(f)

        PRINCIPAL_INFLATION = config_data['principal_inflation']
        RATE_STOCK = config_data['rate_stock']
        RATE_INFLATION = config_data['rate_inflation']
        NUMBER_OF_COMPOUNDS_PER_YEAR = config_data['number_of_compounds_per_year']
        ANNUAL_CONTRIBUTION = config_data['annual_contribution']
    except FileNotFoundError:
        print(f'File {CONFIG_FILE} not found.')
        sys.exit(1)
else:
    print(f'File {CONFIG_FILE} not found.')
    sys.exit(1)

# If PRINCIPAL_STOCK_HISTORY_FILE exists, then use configuration values found there.  Otherwise,
# print an error.

if os.path.isfile(PRINCIPAL_STOCK_HISTORY_FILE):
    try:
        with open(PRINCIPAL_STOCK_HISTORY_FILE) as f:
            config_data = json.load(f)

        PRINCIPAL_STOCK_HISTORY = config_data['principal_stock_history']
    except FileNotFoundError:
        print(f'File {PRINCIPAL_STOCK_HISTORY_FILE} not found.')
        sys.exit(1)
else:
    print(f'File {PRINCIPAL_STOCK_HISTORY_FILE} not found.')
    sys.exit(1)


# Compound Interest Math

# Determine the time in years when compound interest for the stock and compound
# interest for inflation are equal.  Based on the Compound Interest Formula.
def determine_when_stock_and_inflation_are_equal(principal_stock,
                                                 principal_inflation=PRINCIPAL_INFLATION,
                                                 rate_stock=RATE_STOCK,
                                                 rate_inflation=RATE_INFLATION,
                                                 number_of_compounds_per_year=NUMBER_OF_COMPOUNDS_PER_YEAR):
    time_in_years = (1 / number_of_compounds_per_year) * \
                    (log(principal_stock/principal_inflation) /
                     log((number_of_compounds_per_year + rate_inflation) /
                         (number_of_compounds_per_year + rate_stock)))
    return time_in_years


def time_when_goal_reached_with_contribution_no_inflation(principal_stock,
                                                          principal_inflation=PRINCIPAL_INFLATION,
                                                          rate_stock=RATE_STOCK,
                                                          number_of_compounds_per_year=NUMBER_OF_COMPOUNDS_PER_YEAR,
                                                          annual_contribution=ANNUAL_CONTRIBUTION):
    regular_contribution = annual_contribution / number_of_compounds_per_year
    time_in_years = ((1 / number_of_compounds_per_year) *
                     (log(((rate_stock / number_of_compounds_per_year) *
                           (principal_inflation / regular_contribution) + 1) /
                          ((rate_stock / number_of_compounds_per_year) *
                           (principal_stock / regular_contribution) + 1)) /
                      log(1 + (rate_stock / number_of_compounds_per_year))))
    return time_in_years


# Numerical solution using Newton's Method.
# t[i+1] = t[i] - f(t[i]) / f'(t[i])
def time_when_goal_reached_with_contribution_with_inflation(principal_stock,
                                                            principal_inflation=PRINCIPAL_INFLATION,
                                                            rate_stock=RATE_STOCK,
                                                            rate_inflation=RATE_INFLATION,
                                                            number_of_compounds_per_year=NUMBER_OF_COMPOUNDS_PER_YEAR,
                                                            annual_contribution=ANNUAL_CONTRIBUTION):
    regular_contribution = annual_contribution / number_of_compounds_per_year
    time_in_years_i_plus_one = determine_when_stock_and_inflation_are_equal(principal_stock,
                                                                            principal_inflation,
                                                                            rate_stock,
                                                                            rate_inflation,
                                                                            number_of_compounds_per_year) / 2
    time_in_years_i = 0

    while abs(time_in_years_i_plus_one - time_in_years_i) > 0.00001:
        time_in_years_i = time_in_years_i_plus_one
        # What have I done?
        time_in_years_i_plus_one = (time_in_years_i -
                                    ((((rate_stock / number_of_compounds_per_year) *
                                       (principal_stock / regular_contribution) + 1) *
                                      ((1 + (rate_stock / number_of_compounds_per_year)) **
                                       (number_of_compounds_per_year * time_in_years_i))) -
                                     (((rate_stock / number_of_compounds_per_year) *
                                       (principal_inflation / regular_contribution)) *
                                      ((1 + (rate_inflation / number_of_compounds_per_year)) **
                                       (number_of_compounds_per_year * time_in_years_i))) - 1) /
                                    ((number_of_compounds_per_year * ((rate_stock / number_of_compounds_per_year) *
                                     (principal_stock / regular_contribution) + 1) *
                                      ((1 + (rate_stock / number_of_compounds_per_year)) **
                                       (number_of_compounds_per_year * time_in_years_i)) *
                                      (log(1 + (rate_stock / number_of_compounds_per_year)))) -
                                     (number_of_compounds_per_year * ((rate_stock / number_of_compounds_per_year) *
                                      (principal_inflation / regular_contribution)) *
                                      ((1 + (rate_inflation / number_of_compounds_per_year)) **
                                       (number_of_compounds_per_year * time_in_years_i)) *
                                      (log(1 + (rate_inflation / number_of_compounds_per_year))))))

    return time_in_years_i_plus_one


# Graphing

def graph_historical_values(principal_stock_history=PRINCIPAL_STOCK_HISTORY,
                            principal_inflation=PRINCIPAL_INFLATION):
    x_stock_history = [principal_stock_history_dict['date'] for principal_stock_history_dict in principal_stock_history]
    y_stock_history = [principal_stock_history_dict['principal_stock']
                       for principal_stock_history_dict in principal_stock_history]

    plot.plot(x_stock_history, y_stock_history, label='Historical Principal Values')

    plot.xticks(rotation=45)
    plot.hlines(principal_inflation, 0, len(principal_stock_history) - 1, label='Principal Goal')
    plot.legend(loc='center left')
    plot.xlabel('Time')
    plot.ylabel('Principal')

    plot.savefig('image')
    plot.show()


def graph_time_to_goal_no_inflation(principal_stock,
                                    principal_inflation=PRINCIPAL_INFLATION,
                                    rate_stock=RATE_STOCK,
                                    number_of_compounds_per_year=NUMBER_OF_COMPOUNDS_PER_YEAR,
                                    annual_contribution=ANNUAL_CONTRIBUTION):
    regular_contribution = annual_contribution / number_of_compounds_per_year
    time_in_years = time_when_goal_reached_with_contribution_no_inflation(principal_stock,
                                                                          principal_inflation,
                                                                          rate_stock,
                                                                          number_of_compounds_per_year,
                                                                          annual_contribution)

    x_range = numpy.arange(0, time_in_years, 0.1)
    y_range = principal_stock * \
        (1 + rate_stock /
         number_of_compounds_per_year) ** (number_of_compounds_per_year * x_range) + \
        regular_contribution * \
        ((1 + rate_stock /
          number_of_compounds_per_year) ** (number_of_compounds_per_year * x_range) - 1) / \
        (rate_stock / number_of_compounds_per_year)

    plot.plot(x_range, y_range, label='Future Stock Values')
    plot.xlabel('Time')
    plot.ylabel('Principal')

    y_text = principal_stock * \
        (1 + rate_stock /
         number_of_compounds_per_year) ** (number_of_compounds_per_year * time_in_years) + \
        regular_contribution * \
        ((1 + rate_stock /
          number_of_compounds_per_year) ** (number_of_compounds_per_year * time_in_years) - 1) / \
        (rate_stock / number_of_compounds_per_year)
    # plot.text(time_in_years - time_in_years / X_TEXT_SCALING_FACTOR,
    #           y_text + y_text / Y_TEXT_SCALING_FACTOR_YEARS, "{} years".format(round(time_in_years, 1)))
    # plot.text(time_in_years - time_in_years / X_TEXT_SCALING_FACTOR,
    #           y_text - y_text / Y_TEXT_SCALING_FACTOR_DOLLARS, "${:,}".format(round(y_text)))
    plot.text(time_in_years - time_in_years / X_TEXT_SCALING_FACTOR,
              y_text - y_text / Y_TEXT_SCALING_FACTOR_YEARS, "{} years".format(round(time_in_years, 1)))

    plot.savefig('image')
    plot.show()


def graph_stock_vs_inflation_with_payments(principal_stock,
                                           principal_inflation=PRINCIPAL_INFLATION,
                                           rate_stock=RATE_STOCK,
                                           rate_inflation=RATE_INFLATION,
                                           number_of_compounds_per_year=NUMBER_OF_COMPOUNDS_PER_YEAR,
                                           annual_contribution=ANNUAL_CONTRIBUTION):
    regular_contribution = annual_contribution / number_of_compounds_per_year
    time_in_years = time_when_goal_reached_with_contribution_with_inflation(principal_stock,
                                                                            principal_inflation,
                                                                            rate_stock,
                                                                            rate_inflation,
                                                                            number_of_compounds_per_year,
                                                                            annual_contribution)
    # Define total size of the graph.
    x_length = time_in_years + 1
    y_length = (principal_inflation *
                (1 + rate_inflation /
                 number_of_compounds_per_year) ** (number_of_compounds_per_year * x_length))

    # Define ranges/coordinates for stocks, inflation, and text.
    x_stock_range = numpy.arange(0, x_length, 0.1)
    y_stock_range = ((principal_stock *
                      (1 + rate_stock /
                       number_of_compounds_per_year) ** (number_of_compounds_per_year * x_stock_range)) +
                     (regular_contribution *
                      ((1 + rate_stock /
                        number_of_compounds_per_year) ** (number_of_compounds_per_year * x_stock_range) - 1) /
                      (rate_stock / number_of_compounds_per_year)))
    x_inflation_range = numpy.arange(0, x_length, 0.1)
    y_inflation_range = (principal_inflation *
                         (1 + rate_inflation /
                          number_of_compounds_per_year) ** (number_of_compounds_per_year * x_inflation_range))
    x_text = time_in_years
    y_text = (principal_inflation *
              (1 + rate_inflation /
               number_of_compounds_per_year) ** (number_of_compounds_per_year * x_text))

    # Plot points for stocks, inflation, and text.
    plot.plot(x_stock_range, y_stock_range, label='Future Stock Values')
    plot.plot(x_inflation_range, y_inflation_range, label='Future Inflation Values')
    plot.scatter(x_text, y_text)
    # TODO: Be sure this "scaling factor" concept works with edge cases.  I suspect it won't...
    plot.text(x_text - x_length / X_TEXT_SCALING_FACTOR,
              y_text + y_length / Y_TEXT_SCALING_FACTOR_YEARS, "{} years".format(round(x_text, 1)))
    plot.text(x_text - x_length / X_TEXT_SCALING_FACTOR,
              y_text - y_length / Y_TEXT_SCALING_FACTOR_DOLLARS, "${:,}".format(round(y_text)))

    plot.legend()
    plot.xlabel('Years')
    plot.ylabel('Principal')

    plot.savefig('image')
    plot.show()

    # DEBUG
    # print(time_in_years)


def graph_stock_vs_inflation_no_payments(principal_stock,
                                         principal_inflation=PRINCIPAL_INFLATION,
                                         rate_stock=RATE_STOCK,
                                         rate_inflation=RATE_INFLATION,
                                         number_of_compounds_per_year=NUMBER_OF_COMPOUNDS_PER_YEAR):
    time_in_years = determine_when_stock_and_inflation_are_equal(principal_stock,
                                                                 principal_inflation,
                                                                 rate_stock,
                                                                 rate_inflation,
                                                                 number_of_compounds_per_year)
    # Define total size of the graph.
    x_length = time_in_years + 1
    y_length = (principal_stock *
                (1 + rate_stock /
                 number_of_compounds_per_year) ** (number_of_compounds_per_year * x_length))

    # Define ranges/coordinates for stocks, inflation, and text.
    x_stock_range = numpy.arange(0, x_length, 0.1)
    y_stock_range = (principal_stock *
                     (1 + rate_stock /
                      number_of_compounds_per_year) ** (number_of_compounds_per_year * x_stock_range))
    x_inflation_range = numpy.arange(0, x_length, 0.1)
    y_inflation_range = (principal_inflation *
                         (1 + rate_inflation /
                          number_of_compounds_per_year) ** (number_of_compounds_per_year * x_inflation_range))
    x_text = time_in_years
    y_text = (principal_inflation *
              (1 + rate_inflation /
               number_of_compounds_per_year) ** (number_of_compounds_per_year * x_text))

    # Plot points for stocks, inflation, and text.
    plot.plot(x_stock_range, y_stock_range, label='Future Stock Values')
    plot.plot(x_inflation_range, y_inflation_range, label='Future Inflation Values')
    plot.scatter(x_text, y_text)
    # TODO: Be sure this "scaling factor" concept works with edge cases.  I suspect it won't...
    plot.text(x_text - x_length / X_TEXT_SCALING_FACTOR,
              y_text + y_length / Y_TEXT_SCALING_FACTOR_YEARS, "{} years".format(round(x_text, 1)))
    plot.text(x_text - x_length / X_TEXT_SCALING_FACTOR,
              y_text - y_length / Y_TEXT_SCALING_FACTOR_DOLLARS, "${:,}".format(round(y_text)))

    plot.legend()
    plot.xlabel('Years')
    plot.ylabel('Principal')

    plot.savefig('image')
    plot.show()

# graph_stock_vs_inflation_no_payments(PRINCIPAL_STOCK_HISTORY[9]['principal_stock'])
# graph_stock_vs_inflation_with_payments(PRINCIPAL_STOCK_HISTORY[9]['principal_stock'])
# graph_stock_vs_inflation_with_payments(10000, 5000000)
graph_stock_vs_inflation_with_payments(250000, 2000000)
# graph_historical_values()
# graph_time_to_goal_no_inflation(PRINCIPAL_STOCK_HISTORY[9]['principal_stock'])
# graph_time_to_goal_no_inflation(100000)
# time_when_goal_reached_with_contribution_with_inflation(PRINCIPAL_STOCK_HISTORY[9]['principal_stock'])
# time_when_goal_reached_with_contribution_with_inflation(10000, 5000000)

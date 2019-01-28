#!/usr/bin/python3

from math import log
import matplotlib.pyplot as plot
import numpy
import sqlite3
import os
import sys
import json


# Constants

CONFIG_FILE = 'config.json'

# If config.json exists, then use configuration values found there.  Otherwise,
# use the following default constants.

if os.path.isfile(CONFIG_FILE):
    try:
        with open(CONFIG_FILE) as f:
            config_data = json.load(f)

        PRINCIPAL_STOCK = config_data['principal_stock']
        PRINCIPAL_INFLATION = config_data['principal_inflation']
        RATE_STOCK = config_data['rate_stock']
        RATE_INFLATION = config_data['rate_inflation']
        NUMBER_OF_COMPOUNDS_PER_YEAR = config_data['number_of_compounds_per_year']
    except FileNotFoundError:
        print(f'File {CONFIG_FILE} not found.')
        sys.exit(1)
else:
    PRINCIPAL_STOCK = 50000
    PRINCIPAL_INFLATION = 750000
    RATE_STOCK = 0.08
    RATE_INFLATION = 0.03
    NUMBER_OF_COMPOUNDS_PER_YEAR = 12


# Compound Interest Math

# Determine the time in years when compound interest for the stock and compound
# interest for inflation are equal.  Based on the Compound Interest Formula.
def determine_when_stock_and_inflation_are_equal(principal_stock=PRINCIPAL_STOCK,
                                                 principal_inflation=PRINCIPAL_INFLATION,
                                                 rate_stock=RATE_STOCK,
                                                 rate_inflation=RATE_INFLATION,
                                                 number_of_compounds_per_years=NUMBER_OF_COMPOUNDS_PER_YEAR):
    time_in_years = (1 / number_of_compounds_per_years) * \
                    (log(principal_stock/principal_inflation) /
                     log((number_of_compounds_per_years + rate_inflation) /
                         (number_of_compounds_per_years + rate_stock)))
    return time_in_years


# Graphing

def create_stock_vs_inflation_graph(principal_stock=PRINCIPAL_STOCK,
                                    principal_inflation=PRINCIPAL_INFLATION,
                                    rate_stock=RATE_STOCK,
                                    rate_inflation=RATE_INFLATION,
                                    number_of_compounds_per_years=NUMBER_OF_COMPOUNDS_PER_YEAR):
    time_in_years = determine_when_stock_and_inflation_are_equal(principal_stock,
                                                                 principal_inflation,
                                                                 rate_stock,
                                                                 rate_inflation,
                                                                 number_of_compounds_per_years)

    # x coordinates for the stock graph
    x_stock = numpy.arange(0, time_in_years + 1, 0.1)

    # y coordinates for the stock graph using Compound Interest Formula
    y_stock = principal_stock * \
        (1 + rate_stock /
         number_of_compounds_per_years) ** (number_of_compounds_per_years * x_stock)

    # x coordinates for the inflation graph
    x_inflation = numpy.arange(0, time_in_years + 1, 0.1)

    # y coordinates for the inflation graph using Compound Interest Formula
    y_inflation = principal_inflation * \
        (1 + rate_inflation /
         number_of_compounds_per_years) ** (number_of_compounds_per_years * x_inflation)

    # Plotting the points for the stock graph
    plot.plot(x_stock, y_stock, label='Future Stock Values')

    # Plotting the points for the inflation graph
    plot.plot(x_inflation, y_inflation, label='Future Inflation Values')

    # Enable legend.
    plot.legend()

    # Save file locally.
    plot.savefig('image')

    # Function to show the plots for both graphs
    plot.show()

create_stock_vs_inflation_graph()

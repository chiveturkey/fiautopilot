#!/usr/bin/python3

from math import log
import matplotlib.pyplot as plot
import numpy
import sqlite3


# Constants

PRINCIPAL_STOCK = 0
PRINCIPAL_INFLATION = 750000
RATE_STOCK = 0.08
RATE_INFLATION = 0.03
NUMBER_OF_COMPOUNDS_PER_YEAR = 12


# Data Model

# Create Database.
def create_sqlite_db(dbname='fiautopilot.db'):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    # Create table.
    cursor.execute('''CREATE TABLE principal_values
                      (date text, stock real, inflation real)''')

    # Save (commit) the changes, and close the connection.
    connection.commit()
    connection.close()


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

create_stock_vs_inflation_graph(50000)

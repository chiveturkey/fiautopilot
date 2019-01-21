#!/usr/bin/python3

from math import log
import matplotlib.pyplot as plot
import numpy
import sqlite3


# Data Model

# Create Database.
def create_sqlite_db(dbname='fiautopilot.db'):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    # Create table.
    cursor.execute('''CREATE TABLE principal_values
                      (date text, principal real)''')

    # Save (commit) the changes, and close the connection.
    connection.commit()
    connection.close()


# Compound Interest Math

# Determine the time in years when compound interest for the stock and compound
# interest for inflation are equal.  Based on the Compound Interest Formula.
def determine_when_stock_and_inflation_are_equal(principal_stock=0,
                                                 principal_inflation=1000000,
                                                 rate_inflation=0.03,
                                                 rate_stock=0.08,
                                                 number_of_compounds_per_years=12):
    time_in_years = (1 / number_of_compounds_per_years) * \
                  (log(principal_stock/principal_inflation) /
                   log((number_of_compounds_per_years + rate_inflation) /
                       (number_of_compounds_per_years + rate_stock)))
    return time_in_years

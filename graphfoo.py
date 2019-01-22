#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np

# Variables for the Compound Interest Formula
time_in_years = 32
principal_stock = 150000
rate_stock = 0.08
principal_inflation = 750000
rate_inflation = 0.03
number_of_compounds_per_years = 12

# x coordinates for past stock values
x_stock_past = [-3, -2, -1, 0]

# y coordinates for past stock values
y_stock_past = [75000, 100000, 125000, 150000]

# x coordinates for past inflation values
x_inflation_past = [-3, -2, -1, 0]

# y coordinates for past inflation values
y_inflation_past = [750000, 750000, 750000, 750000]

# x coordinates for the stock graph
x_stock = np.arange(0, time_in_years + 1, 0.1)

# y coordinates for the stock graph using Compound Interest Formula
y_stock = principal_stock * \
          (1 + rate_stock /
           number_of_compounds_per_years) ** (number_of_compounds_per_years * x_stock)

# x coordinates for the inflation graph
x_inflation = np.arange(0, time_in_years + 1, 0.1)

# y coordinates for the inflation graph using Compound Interest Formula
y_inflation = principal_inflation * \
              (1 + rate_inflation /
               number_of_compounds_per_years) ** (number_of_compounds_per_years * x_inflation)

# Plotting the past stock points.
plt.plot(x_stock_past, y_stock_past, label='Past Stock Values')

# Plotting the past inflation points.
plt.plot(x_inflation_past, y_inflation_past, label='Past Inflation Values')

# Plotting the points for the stock graph
plt.plot(x_stock, y_stock, label='Future Stock Values')

# Plotting the points for the inflation graph
plt.plot(x_inflation, y_inflation, label='Future Inflation Values')

# Enable legend.
plt.legend()

# Save file locally.
plt.savefig('image')

# Function to show the plots for both graphs
plt.show()

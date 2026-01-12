# This script allows you to plot the results from the Python weather assignment.
# You do not need to understand the contents of this script.
# To run, you can click the run button in your IDE (e.g. right top in Visual Studio Code),
# or you can run `python3 plot_results.py` from your terminal (bash or PowerShell).

import calendar
import json
import os

import pandas as pd
import plotnine as gg
from plotnine import ggplot

months = calendar.month_name[1:]  # Get a list of month names

with open("results.json") as file:
    results = json.load(file)

# Check that actual data was found and loaded, and if not, terminate the script
if not results:
    print("No valid results.json found! Terminating script...")
    exit()


# Convert data to a properly formatted DataFrame
results = pd.json_normalize([{"city": city, **data} for city, data in results.items()])
results["month"] = [months] * len(results)

# Define which properties exist in the dataset
properties = ["month", "total_monthly_precipitation"]
if "relative_monthly_precipitation" in results:
    properties += ["relative_monthly_precipitation"]
data = results.explode(properties)

# Convert data to correct types
data["month"] = pd.Categorical(data["month"], categories=months)
data["total_monthly_precipitation"] = data["total_monthly_precipitation"].astype(float)
if "relative_monthly_precipitation" in data:
    data["relative_monthly_precipitation"] = data["relative_monthly_precipitation"].astype(float)
if "relative_yearly_precipitation" in data:
    data["relative_yearly_precipitation"] = data["relative_yearly_precipitation"].astype(float)

# Ensure the figures folder exists
if not os.path.exists("figures"):
    os.makedirs("figures")

# Bar plot of the precipitation in Seattle per month
figure_1 = (
    ggplot(data=data[data.city == "Seattle"])
    + gg.aes(x="month", y="total_monthly_precipitation")
    + gg.geom_col()
    + gg.theme(axis_text_x=gg.element_text(angle=-30, hjust=0))
    + gg.labs(x=None, y="Precipitation (mm)")
)
figure_1.save("figures/monthly_precipitation_Seattle.pdf")

# Bar plot of the relative precipitation in Seattle per month
if "relative_monthly_precipitation" in data:
    figure_2 = (
        ggplot(data=data[data.city == "Seattle"])
        + gg.aes(x="month", y="relative_monthly_precipitation")
        + gg.geom_col(position=gg.position_dodge())
        + gg.theme(axis_text_x=gg.element_text(angle=-30, hjust=0))
        + gg.labs(x=None, y="Proportion of yearly precipitation")
    )
    figure_2.save("figures/relative_monthly_precipitation_Seattle.pdf")

# Faceted bar plot of the relative monthly precipitation per city,
if "relative_monthly_precipitation" in data and len(data.city.unique()) > 1:
    figure_3a = (
        ggplot(data=data)
        + gg.aes(x="month", y="relative_monthly_precipitation")
        + gg.geom_col(position=gg.position_dodge())
        + gg.theme(axis_text_x=gg.element_text(angle=-30, hjust=0))
        + gg.facet_wrap("city")
        + gg.labs(x=None, y="Proportion of yearly precipitation")
    )
    figure_3a.save("figures/relative_monthly_precipitation.pdf")

# Stacked barplot of the relative yearly precipitation per city.
if "relative_yearly_precipitation" in data:
    figure_3b = (
        ggplot(data=data[data.month == "January"])
        + gg.aes(x=[""], y="relative_yearly_precipitation", fill="city")
        + gg.geom_col()
        + gg.labs(x=None, y="Precipitation (proportion)")
        + gg.scale_x_discrete(labels=[""])
    )
    figure_3b.save("figures/relative_yearly_precipitation.pdf")

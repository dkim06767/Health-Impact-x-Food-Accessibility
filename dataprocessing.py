"""
Daniel Kim, Sophia Kam
This program loads, cleans, and processes all the data necessary
to create the visualizations in the visualizations.py file.
"""

import pandas as pd
import json


def load_food_environment_file(filename: str) -> pd.DataFrame:
    """
    Loads in and returns the data from the Food Enviornment Atlas
    from the given file and filters for the rows that contain data
    for the number of grocery stores per 1,000 people. This method
    also pivots the data so that each county has one row.
    """
    df = pd.read_csv(filename)
    filtered_df = df[df["Variable_Code"] == "GROCPTH20"]
    filtered_wide_df = filtered_df.pivot_table(index=["FIPS"],
                                               columns="Variable_Code",
                                               values="Value")

    return filtered_wide_df.reset_index()


def load_places_file(filename: str) -> pd.DataFrame:
    """
    This file loads and returns the data from the Places county level based
    on the given file. It renames the selected rows, filters the data
    for obesity and diabetes percentages, and pivots the data from length-
    wise to a width-wise format so that each county has one row.
    """

    df = pd.read_csv(filename)
    df = df.rename(
        columns={"StateAbbr": "State",
                 "LocationName": "County",
                 "LocationID": "FIPS"})
    df = df[["State", "County", "Data_Value", "FIPS", "MeasureId"]]
    filtered_df = df[((df["MeasureId"] == "OBESITY") |
                      (df["MeasureId"] == "DIABETES")) &
                     (df["State"] != "US")]
    filtered_wide_df = filtered_df.pivot_table(
        index=["State", "County", "FIPS"], columns="MeasureId",
        values="Data_Value")
    filtered_wide_df = filtered_wide_df.rename(
        columns={"OBESITY": "Obesity", "DIABETES": "Diabetes"})
    return filtered_wide_df.reset_index()


def load_rural_urban_codes_file(filename: str) -> pd.DataFrame:
    """
    Loads and returns the Rural-Urban Continuum codes datasets that is
    inputted in by filtering for only rows that contain data on the values
    and pivots the data so that each county has one row.
    """

    df = pd.read_csv(filename, encoding="cp1252")
    filtered_df = df[df["Attribute"] == "RUCC_2023"].copy()
    filtered_df["Value"] = pd.to_numeric(filtered_df["Value"])
    filtered_wide_df = filtered_df.pivot_table(
        index=["FIPS"], columns="Attribute", values="Value")
    return filtered_wide_df.reset_index()


def load_counties_geojson(filename: str) -> dict:
    """
    Loads and returns county GeoJSON data for the choropleth plots.
    """
    with open(filename) as file:
        return json.load(file)


def load_all_data() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    A method for calling all the other load data functions and merges
    them together. It also removes any missing rows from the 2020
    merged dataset and returns them as a tuple to be called in the
    visualizations file.
    """

    food_env_20 = load_food_environment_file("StateAndCountyData.csv")
    rural_urban_codes_23 = load_rural_urban_codes_file(
        "Ruralurbancontinuumcodes2023.csv")
    places_20 = load_places_file(
        "PLACES__Local_Data_for_Better_Health,"
        "_County_Data_2023_release_20260512.csv")
    places_23 = load_places_file(
        "PLACES__Local_Data_for_Better_Health,"
        "_County_Data,_2025_release_20260430.csv")
    counties = load_counties_geojson("geojson-counties-fips.json")

    # Merges the datasets by year
    df_20 = places_20.merge(food_env_20, on="FIPS", how="left")
    df_23 = places_23.merge(rural_urban_codes_23, on="FIPS", how="left")

    df_20 = df_20[df_20["GROCPTH20"] != -9999]
    return df_20, df_23, counties

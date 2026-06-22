"""
Daniel Kim, Sophia Kam
This program analyzes county-level statistics and creates
visualizations to communicate the relationships between
health outcomes, how rural a county is, and grocery story
access.
"""

import json

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


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


def create_boxplot(df: pd.DataFrame, health_outcome: str) -> None:
    """
    Creates a boxplot with the showing the given health outcome across
    the 9 different rural-urban code values.
    """

    sns.boxplot(x="RUCC_2023", y=health_outcome, data=df)

    plt.xlabel("Rural-Urban Continuum Codes")
    plt.ylabel(f"{health_outcome} Percentage")
    plt.title(f"{health_outcome} Rates by Rural-Urban Continuum Codes")
    plt.figtext(0.5, 0.01, f"This boxplot shows how county {health_outcome}"
                "percentage varies across rural-urban", wrap=True)
    plt.show()


def create_scatterplots(df: pd.DataFrame, health_outcome: str) -> float:
    """
    Creates a scatterplot comparing the number of grocery stores in a county
    per 1,000 people (x-axis) against the percentage of a given health outcome
    (y-axis).
    """
    sns.lmplot(x="GROCPTH20", y=health_outcome, data=df)

    plt.xlabel("Grocery Stores per 1,000 People")
    plt.ylabel(f"{health_outcome} Percentage")
    plt.title(f"{health_outcome} Rates by Number Grocery Stores "
              "per 1,000 People in 2020")
    plt.figtext(0.5, 0.01, "This scatterplot shows the relationship between"
                f"the number of grocery stores and a county {health_outcome}"
                "percentage varies across rural-urban", wrap=True)
    plt.show()

    return np.corrcoef(df["GROCPTH20"], df[health_outcome])[0, 1]


def create_choropleth_map(df: pd.DataFrame, health_outcome: str,
                          outcome_full_str: str, counties: dict) -> None:
    """
    Creates a county-level choropleth map for the given health outcome
    """
    df = df.copy()
    df["FIPS"] = df["FIPS"].astype(str).str.zfill(5)

    fig = px.choropleth_map(
        df, geojson=counties, locations="FIPS", color=health_outcome,
        title=f"{outcome_full_str} by County",
        labels={health_outcome: outcome_full_str}, zoom=3,
        center={"lat": 37.0902, "lon": -95.7129}, opacity=0.5)
    fig.add_annotation(text="This boxplot shows how county"
                       f"{health_outcome} percentage"
                       "varies across rural-urban", x=0.5, y=0.01)
    fig.show()


def main():
    # Loads and cleans the for datasets used for this analysis
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

    # Summary Statistics for 2023 merged Dataset
    print(df_23["Diabetes"].describe())
    print(df_23["Obesity"].describe())
    print(df_23["RUCC_2023"].describe())

    # Summary Statistics for 2020 merged dataset
    print(df_20["Diabetes"].describe())
    print(df_20["Obesity"].describe())
    print(df_20["GROCPTH20"].describe())

    create_boxplot(df_23, "Diabetes")
    create_boxplot(df_23, "Obesity")

    # really small r values, there's no significant relationship between the
    # the health outcomes and the number of grocery stores per 1,000 people
    print(create_scatterplots(df_20, "Diabetes"))
    print(create_scatterplots(df_20, "Obesity"))

    create_choropleth_map(df_23, "RUCC_2023", "Rural-Urban Continuum Codes",
                          counties)
    create_choropleth_map(df_20, "GROCPTH20",
                          "Number Grocery Stores per 1,000 People", counties)


if __name__ == "__main__":
    main()

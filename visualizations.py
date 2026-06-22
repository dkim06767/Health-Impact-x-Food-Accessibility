"""
Daniel Kim, Sophia Kam
This program loads in data from the dataprocessing.py
fild and creates visualizations to communicate the
relationships between health outcomes, how rural a
county is, and grocery story access.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

from dataprocessing import load_all_data


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
                " percentage varies across rural-urban counties", ha="center",
                fontsize=10, wrap=True)
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
                f" the number of grocery stores and a county {health_outcome}"
                " percentage varies across counties", ha="center",
                fontsize=10, wrap=True)
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
    fig.add_annotation(text="This choropleth map shows how county"
                       f" {health_outcome} percentage"
                       " varies across counties in the US",
                       font=dict(size=10), x=0.5, y=0.01)
    fig.show()


def main():
    # Loads all data from the data processing file
    df_20, df_23, counties = load_all_data()

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

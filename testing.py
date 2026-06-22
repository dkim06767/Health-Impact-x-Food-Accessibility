"""
Daniel Kim, Sophia Kam
This program takes the data loaded in from the data processing
file and makes sure that everything is correctly loaded, cleaned,
and merged.
"""

from dataprocessing import load_all_data


def test_loaded_dataframes() -> None:
    """
    Tests to see if the merged dataframes are correctly
    combined as expected
    """
    df_20, df_23, counties = load_all_data()

    # 2020 merged dataset tests
    print(df_20.head())
    print(df_20.columns)
    print(df_20.isnull().sum())

    assert "FIPS" in df_20.columns
    assert "State" in df_20.columns
    assert "County" in df_20.columns
    assert "Obesity" in df_20.columns
    assert "Diabetes" in df_20.columns
    assert "GROCPTH20" in df_20.columns
    assert -9999 not in df_20["GROCPTH20"].values

    # 2023 merged dataset tests
    print(df_23.head())
    print(df_23.columns)
    print(df_23.isnull().sum())

    assert "FIPS" in df_23.columns
    assert "State" in df_23.columns
    assert "County" in df_23.columns
    assert "Obesity" in df_23.columns
    assert "Diabetes" in df_23.columns
    assert "RUCC_2023" in df_23.columns


def main():
    test_loaded_dataframes()


if __name__ == "__main__":
    main()

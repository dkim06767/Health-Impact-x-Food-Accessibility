# Health-Impact-x-Food-Accessibility

## Overview:
This project investigates relationships between county-level health outcomes, rural-urban classification, and grocery store access in the United States. The project uses county-level datasets to compare obesity and diabetes rates with Rural-Urban Continuum Codes and grocery stores per 1,000 people. The final results include summary statistics, boxplots, scatterplots with regression lines, correlation values, and county-level choropleth maps.

Warning- None of the visualizations are meant to provide hard statistical evidence to prove any specific statistical claim between the variables we explore in this project. The plots are simply intended to explore possible patterns between different variables in the data and shouldn't be used as proof of causation or statistical significance. More formal testing would be needed in order to make any further claims.


## Files:
visualizations.py:
This should be the file run in order to examine the visualizations created. It imports data from the dataprocessing.py file. 

dataproessing.py:
This file contains the code necessary to clean, process, and merge the datasets used in this project together. This file doesn't need to be run in order to produce the output.

testing.py:
This file contains the code used to test to make sure all the data was correctly merged together. This file also doesn't need to be used unless there are issues regarding the output. In the case that there are issues, please run through the testing file and make sure that all datasets are properly loaded, cleaned, and merged.


## Downloads:
In order to properly run this file, the following libraries need to be downloaded:
- pandas
- seaborn
- matplotlib.pyplot
- numpy
- plotly.express
- json
These can be done through terminal commands (e.g. pip3 install __). If there are any issues regarding the terminal commands like pip3 not being installed or more, we recommend refering to online resources to learn more.


## Datafiles:
The required datafiles should have already been included when downloading the code, however if there are any issues here are the original links to the data. None of the names of the files should need to be changed and they should all be placed at the same level as the python files:

StateAndCountyData.csv
https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation-downloads

PLACES__Local_Data_for_Better_Health,_County_Data_2023_release_20260512.csv
https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-County-Data-20/h3ej-a9ec/about_data

PLACES__Local_Data_for_Better_Health,_County_Data,_2025_release_20260430
https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-County-Data-20/swc5-untb/about_data

Ruralurbancontinuumcodes2023.csv
https://www.ers.usda.gov/data-products/rural-urban-continuum-codes 


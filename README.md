# project-3

# Recipe Exploration Project

## Overview

This collaborative project focuses on exploring and analyzing recipes data using the Edamam Recipe API. The project involves extracting, transforming, loading (ETL), and performing analyses on the data. Each collaborator is responsible for a specific aspect, including data extraction, loading, Flask route design, and combining code.

## Purpose

The main purpose of this project is to demonstrate a comprehensive ETL workflow using the Edamam Recipe API, SQLite3 databases, and Flask. The goal is to extract relevant recipe data, load it into a SQLite3 database, perform analyses using SQLAlchemy and other libraries, and present the results through Flask web routes. The project aims to showcase diverse recipes, including various cuisines, and provide a well-structured SQLite database containing cleaned and transformed recipe data. Collaboratively developed Python scripts and workflows for future data exploration projects.

## How to Use

Clone the repository to your local machine.
Set up a virtual environment and install all the required dependencies
Run the Flask application using python app.py.
Navigate to the provided routes to interact with the data.

## Ethical Considerations
In the development of this project, ethical considerations have played a pivotal role, particularly in the areas of pulling and analyzing data on Recipes and CO2 Emissions. The team recognizes the importance of responsible data handling and strives to uphold the following ethical principles:

Data Privacy and Security:

The extraction of recipe data respects user privacy and adheres to the terms of service outlined by the Edamam Recipe API. Personal information is handled with utmost care to ensure compliance with privacy regulations.

Environmental Impact Awareness:

Given the nature of CO2 Emissions data, the team is conscious of the potential environmental impact associated with certain ingredients or cooking methods. Efforts are made to present such information responsibly, encouraging awareness rather than contributing to unnecessary concerns.

Data Accuracy and Integrity:

The team is dedicated to maintaining the accuracy and integrity of the data throughout the ETL processes. This includes cross-checking information, handling outliers, and ensuring that insights derived from the data are reliable.

## Required Dependencies
numpy
pandas
dask.dataframe
dask.array
dask.bag
flask
sqlite3
sqlalchemy.ext.automap
sqlalchemy.orm
sqlalchemy
requests
json
pprint
tkinter
dask.distributed

## References for the data source

Edamam Recipe API: https://api.edamam.com/api/recipes/v2

## References
https://examples.dask.org/dataframes/01-data-access.html, https://examples.dask.org/dataframes/02-groupby.html,
https://examples.dask.org/dataframes/03-from-pandas-to-dask.html, were used in order to run the dask client dashboard and also to get groupby and run analysis for the data sets.

# **Finance Analytics Project**

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)

### Description
This code analyses and transforms a database named loan_payments. It enables great incite into this database and provides useful knowledge hidden within.

### Features:
- Extracts data from an RDS database.
- Converts columns into the correct data types.
- Removes/imputes missing values.
- Performs transformations on skewed columns.
- Removes outliers.
- Drops overly corelated columns.
- Analysis database, e.g. losses.

## Installation
Firstly, you must have access to the RDS database, then:
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Open the file: Finance_Project_Compiled.py and run it.

## Usage
1. Simply click the run button.
2. Enjoy learning about the insights from the database.

## File structure
  - ├── credentials.yaml  # Has information on the RDS database location
  - ├── Data_Plots_and_EDA_Transformations.py  # Has classes to plot and transform the data
  - ├── Data_Transformation  # Contains additional transformations
  - ├── Database_Info.py  # Gives general information of the database
  - ├── db_utils.py  # Ignore, old code used for development
  - ├── finalised_loan_paymens_data_numeric.csv  # csv file of database after transformations etc
  - ├── Finance_Project_Compiled.py # Main code
  - ├── RDS_Database_Connector # Class which allows main code to access the RDS Database
  - ├── Timescale_Conversion.py # Changes data type of timebased collumns
  - ├── README.md  # Project documentation

## License
This project is open-source and available under the MIT License. Feel free to use, modify, and distribute it as you see fit, but make sure to provide the appropriate attribution and adhere to the terms of the license.

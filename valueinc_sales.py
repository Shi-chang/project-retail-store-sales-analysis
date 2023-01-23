import pandas as pd

"""
This document processes the data from res/transaction.csv and writes the processed data to res/ValueInc_Cleaned.csv.
"""

# Reads in transaction data from the csv file into the data frame
data = pd.read_csv("res/transaction.csv", sep=';')

# Calculates the profit and markup for each transaction
data['CostPerTransaction'] = data['CostPerItem'] * data['NumberOfItemsPurchased']

data['SalesPerTransaction'] = data['SellingPricePerItem'] * data['NumberOfItemsPurchased']

data['ProfitPerTransaction'] = data['SalesPerTransaction'] - data['CostPerTransaction']

data['Markup'] = round(data['ProfitPerTransaction'] / data['CostPerTransaction'], 2) \
 \
    # Combines day, month and year to form a day-month-year string
day = data['Day'].astype(str)
year = data['Year'].astype(str)

data['date'] = data['Month'] + '-' + day + '-' + year

# Splits the client keywords field
split_col = data['ClientKeywords'].str.split(',', expand=True)

data['ClientAge'] = split_col[0].str.replace('[', '')
data['ClientType'] = split_col[1]
data['LengthOfContract'] = split_col[2].str.replace(']', '')

# Changes the contents of the Description colum to lower case
data['ItemDescription'] = data['ItemDescription'].str.lower()

# Brings in the season data and merges them with the transaction data
seasons = pd.read_csv('res/value_inc_seasons.csv', sep=';')

data = pd.merge(data, seasons, on='Month')

# Drops unnecessary columns
data = data.drop('ClientKeywords', axis=1)
data = data.drop(['Day', 'Month', 'Year'], axis=1)

# Export the processed data into a CSV file
data.to_csv('res/ValueInc_Cleaned.csv', index=False)

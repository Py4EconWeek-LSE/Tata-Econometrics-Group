######################################
#
#   code to clean data and run regressions
#   Python gravity model demonstration
#
######################################

import pandas as pd 
import numpy as np 
import statsmodels.api as sm 

# Helper Functions

def combine_partner_name(x):

    partner_1 = x['exp'] 
    partner_2 = x['imp']

    sorted_list = [partner_1, partner_2]
    sorted_list.sort()
    
    sorted_name = sorted_list[0] + "-" + sorted_list[1] 
    x['partner_1-partner_2'] = sorted_name

    return x

def search_colonial_years(country, colonisation_data):
    if len(colonisation_data[colonisation_data['country_code'] == country]) == 0:
        col_years =  0
    else:
        colonisation_row = colonisation_data[colonisation_data['country_code'] == country]
        col_years  =  float(colonisation_row['colonial_duration'])
    
    return col_years

def create_dummies(row, colonisation_data):

    break_off = 100

    country_1, country_2 = row['partner_1-partner_2'].split('-')

    col_year_list =  [None, None]
    index = 0
    for country in [country_1, country_2]:
        col_years = search_colonial_years(country, colonisation_data)
        col_year_list[index] =  col_years

        index += 1

    if ((col_year_list[0] > 0) & (col_year_list[0] < break_off)) | ((col_year_list[1] > 0) & (col_year_list[1] < break_off)):
        row['either_short_colony'] = 1
    
    if (col_year_list[0] >= break_off) | (col_year_list[1] > break_off):
        row['either_long_colony'] = 1
    
    if ((col_year_list[0] > 0) & (col_year_list[0] < break_off)) & ((col_year_list[1] > 0) & (col_year_list[1] < break_off)):
        row['both_short_colony'] = 1

    if (col_year_list[0] >= break_off) & (col_year_list[1] >= break_off):
        row['both_long_colony'] = 1
    

    return row 

# Download Data
trade_data = pd.read_excel(r'https://www.dropbox.com/s/2uha8rwc8bngcsz/servicesdataset%202.xlsx?dl=1')

colonisation_data = pd.read_excel(r'https://www.dropbox.com/s/216s24p3f8aj8ni/Copy%20of%20Colonial_transformation_data%20%281%29.xls?dl=1')

# some cleaning
colonisation_data_columns = colonisation_data.columns
colonisation_data.rename(columns = {
    'Country Code World Bank' : 'country_code',
    colonisation_data_columns[4] : 'colonial_end_year',
    colonisation_data_columns[5] : 'colonial_duration'
}, inplace = True)

# create trading partners
trade_data = trade_data.apply(combine_partner_name, axis = 1)

# get total trade data for each pair
trade_pairs_total_trade = trade_data.groupby(by = ['partner_1-partner_2'])['trade'].sum().reset_index()

# get trading pair fixed characteristics
trade_pairs_fixed_data = trade_data[['partner_1-partner_2', 'distwces', 'gdp_exp', 'gdp_imp', 'comlang_off', 'comlang_ethno', 'comcol', 'etcr_exp', 'etcr_imp', 'ent_cost_imp', 'ent_cost_exp']].drop_duplicates(subset = ['partner_1-partner_2'])
trade_pairs_fixed_data.rename(columns = {'gdp_exp' : 'gdp_1', 'gdp_imp' : 'gdp_2'}, inplace =  True)

# combine fixed characteristics with total trade data
trade_pairs_combined = pd.merge(trade_pairs_total_trade, trade_pairs_fixed_data, on = 'partner_1-partner_2', how = 'inner')

# tack on colonisation data
trade_pairs_combined['either_short_colony'] = 0
trade_pairs_combined['either_long_colony'] = 0
trade_pairs_combined['both_short_colony'] = 0
trade_pairs_combined['both_long_colony'] = 0

# create colonisation dummies
trade_pairs_combined = trade_pairs_combined.apply(lambda x: create_dummies(x, colonisation_data.copy()), axis = 1)

# Take natural logs of relevant variables
trade_pairs_combined['ln_GDP_1'] = np.log(trade_pairs_combined['gdp_1'])
trade_pairs_combined['ln_GDP_2'] = np.log(trade_pairs_combined['gdp_2'])
trade_pairs_combined['ln_dist'] = np.log(trade_pairs_combined['distwces'])
trade_pairs_combined = trade_pairs_combined[trade_pairs_combined['trade'] != 0]
trade_pairs_combined['ln_trade'] = np.log(trade_pairs_combined['trade'])
# Have to  decide what  to do with no trade, because ln(0) = -infiniy. Temporarily dropped them in line 84
# save the data for visualisation purposes
trade_pairs_combined.to_csv("trading_pairs_data.csv", index =  False)

# Build the regression matrix X and dependent vector y
X = trade_pairs_combined[['ln_GDP_1', 'ln_GDP_2', 'ln_dist', 'either_short_colony', 'either_long_colony', 'both_short_colony', 'both_long_colony', 'comlang_off']]
X['constant'] = 1
y = trade_pairs_combined['ln_trade']

# run regression
regression_1 = sm.OLS(endog=y, exog=X, missing='drop')
regression_1_results = regression_1.fit(cov_type = 'HC1')
regression_1_results.summary()

# any additional regression you would like to run
# manipulate X to your regression form
X[ /column  name/ ] = /some  transformation/

# run regression
regression_2 = sm.OLS(endog=y, exog=X, missing='drop')
regression_2_results = regression_2.fit()
regression_2_results.summary()


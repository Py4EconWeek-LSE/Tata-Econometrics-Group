######################################
#
#   code to produce visualisations
#
#
######################################

import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd  
import plotly.express as px
import numpy as np

trading_pairs_data = pd.read_csv('trading_pairs_data.csv')

def create_colour_mapping(row):

    if row['either_short_colony'] == 1:
        row['mapping_id'] = 1
    elif row['either_long_colony'] == 1:
        row['mapping_id'] = 2
    elif row['both_short_colony'] == 1:
        row['mapping_id'] = 3
    elif row['both_long_colony']:
        row['mapping_id'] = 4
    else:
        row['mapping_id'] = 5

    return row 

plotting_data = trading_pairs_data.apply(create_colour_mapping, axis = 1)

plotting_data['percent_trade'] = 10000000000000 * plotting_data['trade'] / (plotting_data['gdp_1'] + plotting_data['gdp_2'])
plotting_data.dropna(axis = 0, subset  = ['gdp_1', 'gdp_2', 'trade', 'percent_trade', 'ln_dist'], inplace = True)
plotting_data['ln_percent_trade'] = np.log(plotting_data['percent_trade'])
m_overall,b_overall = np.polyfit(x = plotting_data['ln_dist'], y = plotting_data['ln_percent_trade'], deg = 1)

plotting_data['gdp_1_plus_gdp_2'] = plotting_data['gdp_1'] + plotting_data['gdp_2']
plotting_data['ln_gdp_1_plus_gdp_2'] = np.log(plotting_data['gdp_1_plus_gdp_2'])

# Distance vs % Trade (colony status)
fig, ax = plt.subplots(1,1)
for id_num, group in zip([1,5], ['either a short colony', 'neither a colony']):
    group_data = plotting_data[plotting_data['mapping_id']  == id_num]
    m_group, b_group =  np.polyfit(x = group_data['ln_dist'], y = group_data['ln_percent_trade'], deg = 1)
    ax.scatter(x = group_data['ln_dist'], y = group_data['ln_percent_trade'], marker = 'x', alpha = 0.35, label =  group)
    ax.plot(plotting_data['ln_dist'], m_group*plotting_data['ln_dist']+b_group, label = group)
ax.legend()
ax.set_ylim([1, 14])
ax.set_xlabel('$\ln$(distance)')
ax.set_ylabel(r'scaled $\ln(\frac{Trade_{i,j}}{GDP_i+GDP_j})$')
ax.set_title('Distance vs %Trade (Colony Status)')

# Separate Plots
fig, axes =  plt.subplots(1,2, sharex = True, sharey  = True)
ax1, ax2 = axes 
for ax, id_num, group in zip([ax1, ax2], [1,5], ['either short colony', 'neither a colony']):
    group_data = plotting_data[plotting_data['mapping_id']  == id_num]
    m_group, b_group =  np.polyfit(x = group_data['ln_dist'], y = group_data['ln_percent_trade'], deg = 1)
    ax.scatter(x = group_data['ln_dist'], y = group_data['ln_percent_trade'], marker = 'x', alpha = 0.35, label =  group)
    ax.plot(plotting_data['ln_dist'], m_group*plotting_data['ln_dist']+b_group, label = group)
    ax.set_ylim([1, 14])
    ax.set_xlabel('$\ln$(distance)')
    ax.set_ylabel(r'scaled $\ln(\frac{Trade_{i,j}}{GDP_i+GDP_j})$')
    ax.set_title(group)


# Distance vs % Trade (common language)
fig, ax = plt.subplots(1,1)
for id_num, group in zip([1,0], ['common official language', 'not common official']):
    group_data = plotting_data[plotting_data['comlang_off']  == id_num]
    ax.scatter(x = group_data['ln_dist'], y = group_data['ln_percent_trade'], marker = 'x', alpha = 0.35, label =  group)
    m_group, b_group =  np.polyfit(x = group_data['ln_dist'], y = group_data['ln_percent_trade'], deg = 1)
    ax.plot(plotting_data['ln_dist'], m_group*plotting_data['ln_dist']+b_group, label = group)
ax.legend()
ax.set_ylim([1, 14])
ax.set_xlabel('$\ln$(distance)')
ax.set_ylabel(r'scaled $\ln(\frac{Trade_{i,j}}{GDP_i+GDP_j})$')
ax.set_title('Distance vs %Trade (Common Language)')

# GDP vs % Trade (common language)
fig, ax = plt.subplots(1,1)
for id_num, group in zip([1,0], ['common official language', 'uncommon official language']):
    group_data = plotting_data[plotting_data['comlang_off']  == id_num]
    ax.scatter(x = group_data['ln_gdp_1_plus_gdp_2'], y = group_data['ln_trade'], marker = 'x', alpha = 0.35, label =  group)
    m_group, b_group =  np.polyfit(x = group_data['ln_gdp_1_plus_gdp_2'], y = group_data['ln_trade'], deg = 1)
    ax.plot(plotting_data['ln_gdp_1_plus_gdp_2'], m_group*plotting_data['ln_trade']+b_group, label = group)
ax.legend()
ax.set_ylim([-4, 12])
ax.set_xlim([22, 31])
ax.set_xlabel(r'$\ln(GDP_i + GDP_j)$')
ax.set_ylabel(r'scaled $\ln(\frac{Trade_{i,j}}{GDP_i+GDP_j})$')
ax.set_title('GDP of Trading Pair vs %Trade (Common Language)')

# GDP vs % Trade (colony status language)
fig, ax = plt.subplots(1,1)
for id_num, group in zip([1,2,5], ['either_short_colony', 'either_long_colony', 'neither a colony']):
    group_data = plotting_data[plotting_data['mapping_id']  == id_num]
    ax.scatter(x = group_data['ln_gdp_1_plus_gdp_2'], y = group_data['ln_trade'], marker = 'x', alpha = 0.35, label =  group)
    m_group, b_group =  np.polyfit(x = group_data['ln_gdp_1_plus_gdp_2'], y = group_data['ln_trade'], deg = 1)
    ax.plot(plotting_data['ln_gdp_1_plus_gdp_2'], m_group*plotting_data['ln_trade']+b_group, label = group)
ax.legend()
ax.set_ylim([-4, 12])
ax.set_xlim([22, 31])
ax.set_xlabel(r'$\ln(GDP_i + GDP_j)$')
ax.set_ylabel(r'$\ln(trade)$')
ax.set_title('GDP of Trading Pair vs Trade (Common Language)')
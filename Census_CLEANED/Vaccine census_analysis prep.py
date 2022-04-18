import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

vaccine = pd.read_csv('COVID_UID_Vaccine.csv')
census_long = pd.read_csv('complete_census_long.csv')
census_wide = pd.read_csv('complete_census_wide.csv')

#Removing whitespace at end of state names
census_wide['State'] = census_wide['State'].str.rstrip()
census_long['State'] = census_long['State'].str.rstrip()
#Renaming mislabeled columns
col_names = {'Total_x': 'Total Pop', 'Total_y': 'Total Education'}
census_wide = census_wide.rename(columns = col_names)
census_long = census_long.rename(columns = col_names)


#Subsetting vaccine dataset
keep = ['Date', 'Location', 'Distributed', 'Dist_Per_100K', 'Distributed_Per_100k_18Plus',
        'Distributed_Per_100k_65Plus', 'Administered', 'Admin_Per_100K', 'Admin_Per_100k_18Plus',
        'Admin_Per_100k_65Plus', 'Administered_Dose1_Recip', 'Administered_Dose1_Pop_Pct',
        'Administered_Dose1_Recip_18PlusPop_Pct', 'Administered_Dose1_Recip_65PlusPop_Pct',
        'Series_Complete_Yes', 'Series_Complete_Pop_Pct', 'Series_Complete_18PlusPop_Pct', 
        'Series_Complete_65PlusPop_Pct', 'Additional_Doses', 'Additional_Doses_Vax_Pct', 
        'Additional_Doses_18Plus_Vax_Pct', 'Additional_Doses_65Plus_Vax_Pct', 'uid'
          ]
vac_pct = vaccine[keep]
vac_pct.columns.isnull() #No null values in dataset
vac_pct['Location'].unique()
no_loc = ['BP2', 'DD2', 'FM', 'GU', 'IH2', 'LTC', 'MP', 'PW', 'RP', 'VA2', 'VI',
          'MH', 'AS']
vac_pct = vac_pct[~vac_pct['Location'].isin(no_loc)]
len(vac_pct['Location'].unique()) #53 - states + PR, US, and DC

#Keeping only most recent vaccination data
vac_pct = vac_pct[vac_pct.Date == '2022-02-10']
#% Administered that were distributed
vac_pct['Admin/Distrib'] = (vac_pct['Administered'] / vac_pct['Distributed']).round(3)

#Mapping state names to abbreviations
us_state_to_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", 
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", 
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", 
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", 
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC",
    "Puerto Rico": "PR", "United States": "US"
    }
census_wide['Location'] = census_wide['State'].map(us_state_to_abbrev)
census_long['Location'] = census_long['State'].map(us_state_to_abbrev)

#Prep for analysis
census_wide2 = pd.merge(census_wide, vac_pct[['Additional_Doses_Vax_Pct',
                        'Series_Complete_Pop_Pct', 'Admin/Distrib', 'Location']],
                        on = 'Location', how = 'outer')

keep = ['Location','Additional_Doses_Vax_Pct', 'Series_Complete_Pop_Pct', 'Admin/Distrib', 'Proportion under 18',
       'Proportion between 18 and 64', 'Proportion 65 and older', 'Proportion Less than HS',
       'Proportion HS through AA', 'Proportion BA or Higher', 'Percent Estimate']
census_wide2 = census_wide2[keep]
census_wide2 = census_wide2.dropna()
census_wide2['Additional_Doses_Vax_Pct'] = census_wide2['Additional_Doses_Vax_Pct'] / 100
census_wide2['Series_Complete_Pop_Pct'] = census_wide2['Series_Complete_Pop_Pct'] / 100
census_wide2.rename(columns = {'Percent Estimate': 'Poverty Estimate'}, inplace = True)
census_wide2['Poverty Estimate'] = census_wide2['Poverty Estimate'].round(3)

#Export dataset
census_wide2.to_csv('census_wide_final.csv', index = False)


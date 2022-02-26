#Creating wide/long formats of census data

import numpy as np
import pandas as pd

ed = pd.read_csv('education_cleaned.csv')
pov = pd.read_csv('poverty_cleaned.csv')
inc = pd.read_csv('income_cleaned.csv')
age = pd.read_csv('age_sex_cleaned.csv')

#Poverty Data
#New Label group
label = []
for i in range(len(pov)):
    if 'Total' in pov.loc[i,'Label (Grouping)']:
        label.append('Total Estimate')
    else:
        label.append('Below Poverty Estimate')
pov['Label'] = label

#Modifying state column
pov = pov.rename({'Label (Grouping)': 'State', 'Population for whom poverty status is determined':
              'Population of determined status'}, axis = 1)
for i in range(len(pov)):
    if 'Total' in pov.loc[i, 'State']:
        pov.loc[i, 'State'] = pov.loc[i, 'State'].replace('Total Estimate', '')
    else:
        pov.loc[i, 'State'] = pov.loc[i, 'State'].replace('Below poverty level Estimate', '')
#wide format
pov_2 = pov.pivot(index = 'State', columns = 'Label', values = 'Population of determined status')
pov_2['Percent Estimate'] = pov_2['Below Poverty Estimate'] / pov_2['Total Estimate']
pov_2 = pov_2.reset_index()
#long format
pov_long = pov_2.melt(id_vars=['State'])
pov_long = pov_long.rename({'Label': 'Poverty/Total Pop', 'value': 'Poverty/Total Pop Count'}, axis = 1)
#Exported long/wide data format
pov_long.to_csv('poverty_long.csv', index=False)
pov_2.to_csv('poverty_wide.csv', index=False)


#Education Data
#Reformatting, subsetting, and grouping columns
education = ed.transpose()
education = education.rename(columns=education.iloc[0]).drop('Label (Grouping)', axis=0).astype(dtype='float64')
education = education.iloc[:, 0:15]
education["Total"] = education.iloc[:, [0,5]].sum(axis=1) 
education["Less than High School"] = education.iloc[:, [1,6,7]].sum(axis=1)
education["High School through Associates"] = education.iloc[:, [2,3,8,9,10]].sum(axis=1)
education["Bachelor's or Higher"] = education.iloc[:, [4,14]].sum(axis=1)
education = education.iloc[:, -4:]
education["Proportion Less than HS"] = (education.iloc[:,1] / education["Total"]).round(3)
education["Proportion HS through AA"] = (education.iloc[:,2] / education["Total"]).round(3)
education["Proportion BA or Higher"] = (education.iloc[:,3] / education["Total"]).round(3)
education["states"] = education.index.values
education["states"] = education["states"].str.replace('Total Estimate', '')
education = education.sort_values('states')
education = education.reset_index(drop=True)
education = education.rename({'states': 'State'}, axis = 1)
education = education[['State', 'Less than High School', 'Proportion Less than HS', 'High School through Associates',
                       'Proportion HS through AA', "Bachelor's or Higher", 'Proportion BA or Higher', 'Total']]
#long format
education_long = education.melt(id_vars=['State'])
education_long = education_long.rename({'variable': 'Education Level', 'value': 'Education Count'}, axis = 1)
#Export long/wide formats
education.to_csv('education_wide.csv', index=False)
education_long.to_csv('education_long.csv', index=False)


#Income Data - Includes national estimates
#Reformatting, subsetting mean/medians
income = inc.transpose()
income = income.rename(columns=income.iloc[0]).drop('Label (Grouping)', axis=0).astype(dtype='float64')
income_dict = {'Median earnings (dollars) for full-time, year-round workers with earnings': 'Median Income',
               'Mean earnings (dollars) for full-time, year-round workers with earnings': 'Mean Income'}
income.rename(columns=income_dict, inplace=True)
income = income[['Median Income', 'Mean Income']]
income = income.sort_index()
income = income.reset_index().rename({'index': 'State'}, axis=1)
income['State'] = income['State'].str.replace('Total Estimate', '')
#long format
income_long = income.melt(id_vars=['State'])
income_long = income_long.rename({'variable': 'Mean/Median Income', 'value': 'Value'}, axis = 1)
#Export long/wide formats
income.to_csv('income_wide.csv', index=False)
income_long.to_csv('income_long.csv', index=False)


#Age Data
ages = age.transpose()
ages = ages.rename(columns=ages.iloc[0]).drop('Label (Grouping)', axis=0).astype(dtype='float64')
ages = ages.iloc[:, [2,6,10]]
ages["18 to 64 years"] = ages.iloc[:, 1] - ages.iloc[:, 2]
ages = ages[["Under 18 years", "18 to 64 years", "65 years and over"]]
ages['Total'] = ages.iloc[:,0:3].sum(axis=1)
ages['Proportion under 18'] = (ages.iloc[:,0] / ages.iloc[:,3]).round(3)
ages['Proportion between 18 and 64'] = (ages.iloc[:,1] / ages.iloc[:, 3]).round(3)
ages['Proportion 65 and older'] = (ages.iloc[:,2] / ages.iloc[:, 3]).round(3)
ages = ages.sort_index()
ages = ages.reset_index().rename({'index': 'State'}, axis=1)
ages['State'] = ages['State'].str.replace('Total Estimate', '')
#long format
ages_long = ages.melt(id_vars=['State'])
ages_long = ages_long.rename({'variable': 'Age Group', 'value': 'Age Group Count'}, axis = 1)
#Export long/wide formats
ages.to_csv('ages_wide.csv', index=False)
ages_long.to_csv('ages_long.csv', index=False)







({'Label': 'Poverty/Total Pop', 'value_y': 'Poverty/Total Pop Count'})
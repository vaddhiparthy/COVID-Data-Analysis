import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)


#AGE AND SEX 2020 CENSUS DATA
census_agesex = pd.read_csv("US 2020 Census Data_Age and Sex.csv")
census_agesex.columns
    #Keep only total estimates and label columns
census_agesex = census_agesex.loc[:,
       (census_agesex.columns.str.contains('Total')) | (census_agesex.columns.str.contains('Label'))]
    #Remove !! in columns
census_agesex.columns = census_agesex.columns.str.replace('!!', ' ')
    #Keep only selected age categories
census_agesex = census_agesex.iloc[21:33,].reset_index(drop=True)
    #Remove ',' and convert to numeric (float64)
for i in range(len(census_agesex.columns)):
    if i == 0:
        census_agesex.iloc[:, i] = census_agesex.iloc[:, i].str.lstrip()
    else:
        census_agesex.iloc[:, i] = census_agesex.iloc[:, i].replace(',', '', regex=True)
        census_agesex.iloc[:, i] = census_agesex.iloc[:,i].astype(dtype = 'float64')
census_agesex.dtypes


#EDUCATION 2020 CENSUS DATA
census_education = pd.read_csv("US 2020 Census Data_Education.csv")
census_education.columns
census_education['Label (Grouping)']
    #Keep only Total Estimates and Label columns
census_education = census_education.loc[:, 
       (census_education.columns.str.contains('Total')) | (census_education.columns.str.contains('Label'))]
    #Remove !! in columns
census_education.columns = census_education.columns.str.replace('!!', ' ')
    #Select only education data by age
census_education = census_education.iloc[1:28].reset_index(drop=True)
    #Remove ',' and convert to numeric (float64)
for i in range(len(census_education.columns)):
    if i == 0:
        census_education.iloc[:, i] = census_education.iloc[:, i].str.lstrip()
    else:
        census_education.iloc[:, i] = census_education.iloc[:, i].replace(',', '', regex=True)
        census_education.iloc[:, i] = census_education.iloc[:,i].astype(dtype = 'float64')
census_education.dtypes


#INCOME 2020 CENSUS DATA - DOES NOT INCLUDE PART-TIME WORKERS
census_income = pd.read_csv("US 2020 Census Data_Income.csv")
census_income.columns
census_income['Label (Grouping)']
    #Remove !! in columns
census_income.columns = census_income.columns.str.replace('!!', ' ')
    #Remove misc metrics
census_income = census_income.iloc[2:12].reset_index(drop=True)
    #Include only total household data
census_income = census_income.loc[:, 
        (census_income.columns.str.contains('Total')) | (census_income.columns.str.contains('Label'))]
     #Remove % and , in strings then comvert values to numeric (float64)   
for i in range(len(census_income.columns)):
    if i == 0:
        census_income.iloc[:, i] = census_income.iloc[:, i].str.lstrip()
    else:    
        census_income.iloc[:, i] = census_income.iloc[:, i].replace('%', '', regex=True)
        census_income.iloc[:, i] = census_income.iloc[:, i].replace(',', '', regex=True)
        census_income.iloc[:, i] = census_income.iloc[:, i].astype(dtype = 'float64')
census_income.dtypes


#POVERTY 2020 CENSUS DATA - ONLY INCLUDES VERIFIED POVERTY STATUSES
census_poverty = pd.read_csv("US 2020 Census Data_Poverty.csv")
census_poverty.columns
census_poverty['Label (Grouping)']
    #Remove !! in columns
census_poverty.columns = census_poverty.columns.str.replace('!!', ' ')
    #Remove percent categories
census_poverty = census_poverty.loc[:, ~census_poverty.columns.str.contains('Percent')]
    #Keep only total estimates and reformatting dataframe
census_poverty = census_poverty.iloc[0,:].to_frame()
census_poverty.reset_index(inplace=True)
census_poverty = census_poverty.rename(columns=census_poverty.iloc[0])
census_poverty = census_poverty.iloc[1:, :].reset_index(drop=True)
    #Remove ',' and convert values to numeric (float64)
for i in range(len(census_poverty.columns)):
    if i != 0:
        census_poverty.iloc[:, i] = census_poverty.iloc[:, i].replace(',', '', regex=True)
        census_poverty.iloc[:, i] = census_poverty.iloc[:, i].astype(dtype = 'float64')

#Export cleaned datasets as .csv
census_agesex.to_csv('age_sex_cleaned.csv', index=False)
census_education.to_csv('education_cleaned.csv', index=False)
census_income.to_csv('income_cleaned.csv', index=False)        
census_poverty.to_csv('poverty_cleaned.csv', index=False)
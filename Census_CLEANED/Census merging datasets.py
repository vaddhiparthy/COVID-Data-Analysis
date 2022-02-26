#Combining Census Datasets
import numpy as np
import pandas as pd
from functools import reduce
pd.set_option('display.max_columns', None)

#Wide format
age_wide = pd.read_csv('ages_wide.csv')
edu_wide = pd.read_csv('education_wide.csv')
inc_wide = pd.read_csv('income_wide.csv')
pov_wide = pd.read_csv('poverty_wide.csv')
#List
df_wide = [age_wide, edu_wide, inc_wide, pov_wide]
df_wide
#Complete datset
census_wide = reduce(lambda left,right: pd.merge(left,right, on=['State'], how='outer'), df_wide)


#Long format
age_long = pd.read_csv('ages_long.csv')
edu_long = pd.read_csv('education_long.csv')
inc_long = pd.read_csv('income_long.csv')
pov_long = pd.read_csv('poverty_long.csv')
#List
df_long = [age_long, edu_long, inc_long, pov_long]
#Complete dataset
census_long = reduce(lambda left,right: pd.merge(left, right, on=['State'], how='outer'), df_long)

#Export datasets
census_wide.to_csv('complete_census_wide.csv', index=False)
census_long.to_csv('complete_census_long.csv', index=False)

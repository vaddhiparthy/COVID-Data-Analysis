#Project Visualizations
import numpy as np
import pandas as pd

#Loading cleaned datasets
age_clean = pd.read_csv('age_sex_cleaned.csv')
edu_clean = pd.read_csv('education_cleaned.csv')
income_clean = pd.read_csv('income_cleaned.csv')
pov_clean = pd.read_csv('poverty_cleaned.csv')

#Loading CDC Case data
vaccine = pd.read_csv('Vaccine.csv')
vaccine["Date"] = pd.to_datetime(vaccine["Date"], format='%m/%d/%Y')
    #Selecting total cases as of 02/09/2022
vac_total = vaccine[vaccine['Date'] == '2022-02-10 00:00:00'].reset_index(drop=True)
vac_total = vac_total.sort_values(by='Location').iloc[:,[2,14,15]].reset_index(drop=True)
vac_total['Administered 18-64'] = vac_total['Administered_18Plus'] - vac_total['Administered_65Plus']
#Reformatting for visualization - Ages
ages = age_clean.transpose()
ages = ages.rename(columns=ages.iloc[0]).drop('Label (Grouping)', axis=0).astype(dtype='float64')
ages = ages.iloc[:, [2,6,10]]
ages["18 to 64 years"] = ages.iloc[:, 1] - ages.iloc[:, 2]
ages = ages[["Under 18 years", "18 to 64 years", "65 years and over"]]
ages['Total'] = ages.iloc[:,0:3].sum(axis=1)
ages['Proportion under 18'] = (ages.iloc[:,0] / ages.iloc[:,3]).round(3)
ages['Proportion between 18 and 64'] = (ages.iloc[:,1] / ages.iloc[:, 3]).round(3)
ages['Proportion 65 and older'] = (ages.iloc[:,2] / ages.iloc[:, 3]).round(3)
ages['Location'] = ages.index.values
ages['Location'] = ages['Location'].str.replace('Total Estimate', '')


#Reformatting for visualization - Education
education = edu_clean.transpose()
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


#Reformatting for visualization - Income
income = income_clean.transpose()
income = income.rename(columns=income.iloc[0]).drop('Label (Grouping)', axis=0).astype(dtype='float64')
income_dict = {'Median earnings (dollars) for full-time, year-round workers with earnings': 'Median Income',
               'Mean earnings (dollars) for full-time, year-round workers with earnings': 'Mean Income'}
income.rename(columns=income_dict, inplace=True)


#Plotting
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style = 'darkgrid')

#Multiple boxplot of education level proportions
plt.figure(dpi= 600)
sns.boxplot(data=education.iloc[:,4:7], orient='h').set(xlabel = 'Percent of Total Education')
plt.title("Education Levels for US States, D.C., and Puerto Rico")

#Mean and median boxplots
plt.figure(dpi= 600)
sns.boxplot(data=income.iloc[:52, 10:13], orient='h').set(xlabel = 'USD ($)')
plt.title("Income Levels for US States, D.C., and Puerto Rico")

plt.figure(dpi=600)
sns.histplot(data=income, x ="Mean Income", color="orange", label="Mean Income", kde=True)
sns.histplot(data=income, x = "Median Income", color="blue", label="Median Income", kde=True)
plt.xlabel("USD ($)")
plt.title("Historgrams of Income for US States, D.C., and Puerto Rico")
plt.legend()

plt.figure(dpi=600)
sns.boxplot(data=ages.iloc[:,4:7], orient='h').set(xlabel = 'Percent of Total Population')
plt.title("Age Levels for US States, D.C., and Puerto Rico")

# COVID Data Analysis

The project presents the COVID-19 situation in the United States until March 2022 using the most reliable sources of data. Various metrics used by the public when they are having a conversation about the COVID-19 situation have been identified.

The relevant reliable sources of the data have been identified and the data has been processed using various mathematical and programming tools at our disposal, the primary challenge was to match various updates for a specific time that had different update timestamps which made it challenging for joining the data from various datasets. The MMWR was could not be used and hence unique identifier (UID) was formulated to uniquely identify the data gathered for a week. This was further met with the challenges of choosing the right way of aggregating the data during a specific week. One more challenge was choosing the features, especially from the hospital dataset which had 109 features.

The data aggregation had a weekly resolution when presenting the visualization on various COVID-19 metrics and the ARIMA model for predicting the COVID19 cases performed poorly on this weekly data hence resolution was improved by using daily data from the CDC.

The results are visualizations of various metrics and statistical analysis results when considering their interdependencies and variation along the time axis. The ARIMA model tuning and analysis of the error metrics have pointed toward increasing the data resolution from weekly to daily data points which resulted in an accurate ARIMA model.

### Files here show:
#### Various Datasets (Primarily from CDC)
#### Project Report
#### ARIMA Model Accuracy Report
#### Jupyter Notebook with the below:
##### Data wrangling
##### Data cleaning
##### Feature engineering and exploratory data analysis
##### ARIMA modeling and beta regressions

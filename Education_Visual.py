import csv
import pandas as pd
import matplotlib.pyplot as plt

# read the CSV file to prepare a dataframe with the paramters of 4-Year Graduation Rate and its associated metric score
graduationRates = pd.read_csv('/Users/tanishadutta/Downloads/JPMC Hackathon/Education Data/SDP_Graduation_Rates.csv')
graduationRates = graduationRates[(graduationRates['rate_type'] == '4-Year Graduation Rate') & (graduationRates['score'].str.replace('.', '', regex=False).str.isnumeric())]
graduationRates['score'] = pd.to_numeric(graduationRates['score'], errors='coerce')
graduationRates = graduationRates.dropna(subset=['score'])
graduationRates = graduationRates.drop(['sector', 'denom', 'num', 'group', 'subgroup'], axis=1)

# group the data from graduationRates by cohort year and school ULCS ID to calculate mean of scores for 4-Year Graduation
grouped_data = graduationRates.groupby(['cohort', 'schoolid_ulcs'])['score'].mean().unstack()

# only read ULCS Code and Zip Code from school master list CSV
columns_include = ['ULCS Code', 'Zip Code']
schoolList = pd.read_csv('/Users/tanishadutta/Downloads/JPMC Hackathon/Education Data/2023-2024 Master School List.csv', usecols=columns_include)

# combine and merge the two dataframes from the two CSVs via their mutual column: ULCS ID
combined_df = pd.concat([graduationRates, schoolList], ignore_index=True)
schoolList = schoolList.rename(columns={'ULCS Code': 'schoolid_ulcs'}) 
merged_df = pd.merge(graduationRates, schoolList, on='schoolid_ulcs')

# calculate the average scores by metric by zip code
avg_scores_by_zip = merged_df.groupby('Zip Code')['score'].mean()

# create bar plot of the Average 4-Year Graduation Rate by Zip Code
plt.figure(figsize=(10, 6))
avg_scores_by_zip.plot(kind='bar',color='orange',)
plt.xlabel('Zip Code')
plt.ylabel('Average 4-Year Graduation Rate')
plt.title('Average 4-Year Graduation Rate by Zip Code')
plt.xticks(rotation=45)
plt.show()

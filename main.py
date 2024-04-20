import csv
import pandas as pd
import matplotlib.pyplot as plt

graduationRates = pd.read_csv('/Users/tanishadutta/Downloads/JPMC Hackathon/Education Data/SDP_Graduation_Rates.csv')
graduationRates = graduationRates[(graduationRates['rate_type'] == '4-Year Graduation Rate') & (graduationRates['score'].str.replace('.', '', regex=False).str.isnumeric())]
graduationRates['score'] = pd.to_numeric(graduationRates['score'], errors='coerce')
graduationRates = graduationRates.dropna(subset=['score'])
graduationRates = graduationRates.drop(['sector', 'denom', 'num', 'group', 'subgroup'], axis=1)
grouped_data = graduationRates.groupby(['cohort', 'schoolid_ulcs'])['score'].mean().unstack()

columns_include = ['ULCS Code', 'Zip Code']
schoolList = pd.read_csv('/Users/tanishadutta/Downloads/JPMC Hackathon/Education Data/2023-2024 Master School List.csv', usecols=columns_include)

combined_df = pd.concat([graduationRates, schoolList], ignore_index=True)
schoolList = schoolList.rename(columns={'ULCS Code': 'schoolid_ulcs'}) 
print(schoolList.columns)
print(graduationRates.columns)

merged_df = pd.merge(graduationRates, schoolList, on='schoolid_ulcs')

avg_scores_by_zip = merged_df.groupby('Zip Code')['score'].mean()

plt.figure(figsize=(10, 6))
avg_scores_by_zip.plot(kind='bar',color='orange',)
plt.xlabel('Zip Code')
plt.ylabel('Average 4-Year Graduation Rate')
plt.title('Average 4-Year Graduation Rate by Zip Code')
plt.xticks(rotation=45)
plt.show()

# text cleaning for the company names
import pandas as pd

filepath = 'CINDERELA/LMA data/ORBIS queries/'
filename = 'Companies_CDW_Cinderela'
column = 'Name'
with_index = False

xlsx = pd.read_excel(filepath + filename + '.xlsx')
#data cleaning
xlsx[column] = xlsx[column].str.upper()
xlsx[column] = xlsx[column].str.replace('BV', '')
xlsx[column] = xlsx[column].str.replace('B.V.', '')
xlsx[column] = xlsx[column].str.strip()
xlsx.drop_duplicates(subset= column, inplace = True)

xlsx.to_excel(filepath + filename + '_cleaned.xlsx',
              encoding='utf-8',
              index=with_index)

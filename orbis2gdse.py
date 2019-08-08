# converts an ORBIS output file into a GDSE Actors input table
# multiple ORBIS files can be combined into a single one if they are placed in the same folder

import pandas as pd
import os

# #### I N P U T #### #

# choose the directory where ORBIS exports are located (it should not contain any other files)
fpath = '/Users/rusnesileryte/Downloads/Amsterdam/T3.2_Actors_CDW/ORBIS_by_activity_and_region/ORBIS_exports/'
# choose output filename
outfile = "T3.2_Actors.xlsx"

# #### S C R I P T #### #

actor_tables = []
for f in os.listdir(fpath):
    if '~' in f: #skip temporary files if a file is open in excel
        continue
    elif '.xlsx' in f:
        print f
        orbis = pd.read_excel(fpath + f, sheet_name='Results')

        GDSE_columns = ['BvDid', 'name', 'NACE', 'Code', 'Year', 'Description english',
                        'Description original', 'BvDii', 'Website', 'Employess',
                        'Turnover', 'Postcode', 'Address', 'City', 'Country', 'wkt']

        orbis = orbis[['BvD ID number',
                       'Company name',
                       'NACE Rev. 2\nCore code (4 digits)',
                       'Cons.\ncode',
                       'Last\navail.\nyear',
                       'Trade description (English)',
                       'Trade description in original language',
                       'BvD Independence Indicator',
                       'Website address',
                       'Number of employees (last value)',
                       'Operating revenue (Turnover) (last value)\nth EUR',
                       'Postcode',
                       'Street, no., building etc, line 1',
                       'City',
                       'Country']]
        orbis['wkt'] = ''

        orbis.columns = GDSE_columns
        actor_tables.append(orbis)

tables = pd.concat(actor_tables)
print len(tables.index), 'actors have been written into a GDSE compatible table'

tables.to_excel(fpath + outfile, encoding='utf-8', index=False)

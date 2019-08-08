# takes ORBIS batch search output files and combines them into ones
# outputs LMA name + ORBIS details required by the GDSE template

import pandas as pd
import os
import re
import numpy as np

import warnings #ignore unnecessary warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)
pd.options.mode.chained_assignment = None


def to_actor_table(fpath, fname):
    # takes an ORBIS export file and returns a GDSE actor table
    orbis = pd.read_excel(fpath + fname, sheet_name='Results')

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
    return orbis


def extract_huisnr(address):
    # extracts house number from an address
    address = str(address)
    items = re.split('-| ', address)
    for item in items:
        if item.isdigit():
            return item



# choose PROJECT: REPAiR or CINDERELA
while True:
    project = raw_input('Choose project: REP or CIN\n')
    if project == 'REP':
        projectname = 'REPAiR'
        break
    elif project == 'CIN':
        projectname = 'CINDERELA'
        break
    else:
        print 'Wrong choice.'

# choose scope: Food Waste or Construction & Demolition Waste
while True:
    scope = raw_input('Choose scope: CDW or FW\n')
    if scope == 'CDW' or scope == 'FW':
        break
    else:
        print 'Wrong choice.'

InputFolder = '{0}/LMA data/Exports_{1}_ORBIS/'.format(projectname, scope)
OutputFolder = '{0}/LMA data/Input_{1}_part2/'.format(projectname, scope)

actor_tables = []
summary_tables = []
for f in os.listdir(InputFolder):
    if '~' in f: #skip temporary files if a file is open in excel
        continue
    elif "results.xlsx" in f:
        print f
        table = to_actor_table(InputFolder, f)
        actor_tables.append(table)

        smm = f.replace('_results', '')
        summary_tables.append(pd.read_excel(InputFolder + smm))

summary = pd.concat(summary_tables)
summary = summary[summary['Company name'] != 'Name']
total = len(summary.index)
summary.dropna(subset=['Matched bvdid'], inplace=True)
summary = summary[['Company name', 'Matched bvdid']]
summary.rename(columns={'Company name': 'LMA Name',
                        'Matched bvdid': 'BvDid'}, inplace=True)
found = len(summary.index)
print 'Out of {0} actors, {1} have been found during ORBIS batch search'.format(total, found)

tables = pd.concat(actor_tables)
tables.drop_duplicates(subset=['BvDid'], inplace=True)

# extract house number from the address
tables['Huisnummer'] = tables['Address'].apply(lambda x: extract_huisnr(x))
# skip those entries that do not have a NACE code as they do not serve the purpose

# rewrite NACE to include the activity group e.g. 3821 to E-3821
nace_table = pd.read_excel('{0}/LMA data/NACE_table.xlsx'.format(projectname))
nace_table = nace_table[['Digits', 'Code']]
nace_table.rename(columns={'Code':'NACE code'}, inplace=True)
nace_table_merged = pd.merge(tables, nace_table, how='left', left_on='NACE', right_on='Digits')

nace_table_merged.drop(columns=['NACE', 'Digits'], inplace=True)
nace_table_merged.rename(columns={'NACE code': 'NACE'}, inplace=True)
tables = nace_table_merged.copy()

# check if all nace codes have been found
no_nace = tables[tables['NACE'] == np.NaN]
if len(no_nace.index) > 0:
    print 'WARNING! not all NACE codes have been found in the NACE table'


# export LMA actors with their corresponding ORBIS companies according to batch search
merged = pd.merge(tables, summary, on="BvDid")
merged.rename(columns={'name': 'ORBIS name'})

merged.dropna(subset=['NACE'], inplace=True)
print found - len(merged.index), 'matches have been removed due to the missing NACE code'

merged.to_excel(OutputFolder + "ORBIS_by_name.xlsx", encoding='utf-8', index=False)


orbis_by_name = tables[['BvDid', 'name', 'NACE', 'Year', 'Country', 'City', 'Postcode',
                        'Address', 'Huisnummer']]

# unify column names between the two tables
orbis_by_nace = pd.read_excel(OutputFolder + 'ORBIS_by_nace.xlsx')
orbis_by_name.columns = orbis_by_nace.columns

# concatenate all ORBIS actors into a single table
orbis_all = pd.concat([orbis_by_nace, orbis_by_name])
orbis_all.drop_duplicates(subset=['BvDid'], inplace=True)

orbis_all.to_excel(OutputFolder + "ORBIS_all.xlsx", encoding='utf-8', index=False)

# print some statistics
nace_count = len(orbis_by_nace.index)
name_count = len(orbis_by_name.index)
all_count = len(orbis_all.index)

print nace_count, 'actors have been selected by relevant NACE codes'
print name_count, 'actors have been found usinf batch search'
print all_count, 'actors make up the final set of ORBIS actors'

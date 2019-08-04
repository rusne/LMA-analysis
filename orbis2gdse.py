# converts an ORBIS output file into a GDSE Actors input table
# multiple ORBIS files can be combined into a single one

import pandas as pd
import os
import numpy as np


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

def to_activity_table(fpath, fname):
    # extracts a list of activities 
    pass


#choose PROJECT: REPAiR or CINDERELA
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

#choose scope: Food Waste or Construction & Demolition Waste
while True:
    scope = raw_input('Choose scope: CDW or FW\n')
    if scope == 'CDW' or scope == 'FW':
        break
    else:
        print 'Wrong choice.'

filepath = '{0}/LMA data/Exports_{1}_ORBIS/'.format(projectname, scope)

actor_tables = []
summary_tables = []
for f in os.listdir(filepath):
    if '~' in f: #skip temporary files if a file is open in excel
        continue
    elif "results.xlsx" in f:
        print f
        table = to_actor_table(filepath, f)
        actor_tables.append(table)

        smm = f.replace('_results', '')
        summary_tables.append(pd.read_excel(filepath + smm))

summary = pd.concat(summary_tables)
summary = summary[summary['Company name'] != 'Name']
total = len(summary.index)
summary.dropna(subset=['Matched bvdid'], inplace=True)
found = len(summary.index)
print 'Out of {0} actors, {1} have been found during ORBIS batch search'.format(total, found)

tables = pd.concat(actor_tables)
print len(tables.index), 'actors have been written into a GDSE compatible table'

tables.to_excel(filepath + "T3.2_Actors_LMA_ORBIS.xlsx", encoding='utf-8', index=False)
summary.to_excel(filepath + "ORBIS_by_name.xlsx", encoding='utf-8')

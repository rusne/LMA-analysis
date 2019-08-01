import os #use to create new folders and change in between different folders

import pandas as pd #python data analysis library

import numpy as np #python scientific computing library

import warnings #ignore unnecessary warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)
pd.options.mode.chained_assignment = None

#_________________________________________________

# 0.a )  C H O O S I N G   P R O J E C T
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

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

#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

# 0.b )  R E A D I N G   F I L E S
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

#choose scope: Food Waste or Construction & Demolition Waste
while True:
    scope = raw_input('Choose scope: CDW or FW\n')
    if scope == 'CDW' or scope == 'FW':
        break
    else:
        print 'Wrong choice.'


Exportfolder = "{0}/LMA data/Exports_{1}_part2".format(projectname, scope)
if not os.path.exists(Exportfolder): # create folder if it does not exist
    os.makedirs(Exportfolder)

DataFolder = "LMA data".format(scope)
os.chdir(DataFolder) # change to Part 1 folder

#_________________________________________________________
# 0.c) M O D E L L I N G   V A R I A B L E S
#_________________________________________________________

#_________________________________________________________
 #0.C) Reading in the Comprehensive table from Part 1
 #_________________________________________________________

# LMA = pd.read_excel('Exports_{0}_part1/Export_LMA_Analysis_comprehensive_part1.xlsx'.format(scope))
LMA_actors = pd.read_excel('Exports_{0}_part1/Export_LMA_actors.xlsx'.format(scope))
LMA_actors_w_postcode = pd.read_excel('Exports_{0}_part1/Export_LMA_actors.xlsx'.format(scope))

LMA_actors.replace(np.NaN, '',inplace=True) #data cleaning

# create a unique key for LMA actors: Name + Postcode
LMA_actors['LMA_key'] = LMA_actors['Name'] + ' ' + LMA_actors['Postcode']

LMA_actors.to_excel('lma_key.xlsx')

#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
# 2 )  F U N C T I O N S
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________


def give_bvdid(ind, scope, start_bvd):
    bvdid = 'LMA' + scope + str(ind + start_bvd).zfill(5)
    return bvdid


def chain_order(role):
    if role == 'ontdoener':
        return 0
    elif role == 'inzamelaar':
        return 1
    elif role == 'ontvanger':
        return 2
    elif role == 'verwerker':
        return 3
    else:
        print 'error: unknown role has been found  ', role


def give_nace(role):
    nace_by_role = {'ontdoener': 'WU-0004',
                    'inzamelaar': 'WU-0005',
                    'ontvanger': 'WU-0006',
                    'verwerker': 'WU-0007'}
    return nace_by_role[role]

#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
# 3 a & b & c )  C O N N E C T I N G   O R B I S    W I T H    L M A
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
#######
# STEP 3 a
#######

#_________________________________________________________
#       a) For connecting the LMA database with the Orbis exports based on address
#_________________________________________________________


#reading in the Actors Orbis data exported from the GDSE

ORBIS_all = pd.read_excel('Exports_{0}_part1/ORBIS_all.xlsx'.format(scope))
ORBIS_all = ORBIS_all[['Name', 'Postcode', 'BvDid', 'NACE', 'City', 'Huisnummer', 'Year']]


#data cleaning
ORBIS_all['Postcode'] = ORBIS_all['Postcode'].str.replace(' ','')
ORBIS_all['Postcode'] = ORBIS_all['Postcode'].str.upper()

ORBIS_all.rename(columns={'Huisnummer':'Huisnr', 'Name':'ORBIS_name'},inplace=True)

# override entries that do not have house number at all with 0
ORBIS_all['Huisnr'].replace(np.NaN,0,inplace=True)
# ORBIS_all = ORBIS_all[ORBIS_all['Huisnr']!=999999] #filter out the entries that do not have a housenumber assigned
ORBIS_all['Huisnr'] = ORBIS_all['Huisnr'].astype(int)
ORBIS_all.replace(np.NaN, '',inplace=True) #data cleaning

# BVDid_NACE_postcode_huisnr=BVDid_NACE_postcode_huisnr.reset_index() #EDITED
# del BVDid_NACE_postcode_huisnr['index'] #EDITED



# Merge LMA data with the Orbis export to connect the postcode, huisnummers with a BVDid to eventually get a NACE code per waste entry
LMA_actors['Huisnr'] = pd.to_numeric(LMA_actors['Huisnr'], errors='coerce') #making sure the datatypes for Huisnummer is the same for the two merged dataframes
LMA_Orbis_by_address = pd.merge(LMA_actors,ORBIS_all,on=['Postcode','Huisnr'],how='left')

LMA_Orbis_by_address.rename(columns={'BvDid':'BvDid_by_address', 'NACE':'NACE_by_address',
                                     'Postcode': 'LMA_postcode', 'Plaats': 'LMA_plaats',
                                     'Straat': 'LMA_straat', 'Huisnr':'LMA_huisnr', 'City': 'LMA_city',
                                     'ORBIS_name': 'ORBIS_name_by_address', 'Year':'Year_by_address'}, inplace=True)
LMA_Orbis_by_address.drop_duplicates(inplace=True)


#_________________________________________________________
#       b) For connecting the LMA database with the Orbis exports based on company name
#_________________________________________________________


ORBIS_by_name = pd.read_excel('Exports_{0}_part1/ORBIS_by_name.xlsx'.format(scope))
ORBIS_by_name = ORBIS_by_name[['Company name', 'Matched bvdid']]
ORBIS_by_name.rename(columns={'Company name':'Name', 'Matched bvdid':'BvDid'},inplace=True)

#data cleaning
ORBIS_by_name['Name'] = ORBIS_by_name['Name'].str.upper()
ORBIS_by_name['Name'] = ORBIS_by_name['Name'].str.replace('BV', '')
ORBIS_by_name['Name'] = ORBIS_by_name['Name'].str.replace('B.V.', '')
ORBIS_by_name['Name'] = ORBIS_by_name['Name'].str.strip()
ORBIS_by_name.drop_duplicates(subset= 'Name', inplace = True)

# Merge Orbis export based on batch search in ORBIS with the overall database
ORBIS_by_name_wNACE = pd.merge(ORBIS_by_name, ORBIS_all, on=['BvDid'], how='inner', validate='m:1')
ORBIS_by_name_wNACE.replace(np.NaN, '',inplace=True) #data cleaning
ORBIS_by_name_wNACE.rename(columns={'ORBIS_name': 'ORBIS_name_by_name',
                                   'Postcode': 'ORBIS_postcode', 'City': 'ORBIS_city', 'Huisnr': 'ORBIS_huisnr',
                                   'NACE': 'NACE_by_name', 'Year': 'Year_by_name'}, inplace=True)

# Merge LMA data with ORBIS based on the batch search on company names in ORBIS
actors_full_merge = pd.merge(LMA_Orbis_by_address, ORBIS_by_name_wNACE, on=['Name'], how = 'left')
actors_full_merge.replace(np.NaN, '', inplace=True) #data cleaning
actors_full_merge.rename(columns={'BvDid': 'BvDid_by_name'}, inplace=True)
actors_full_merge.drop_duplicates(inplace=True)


#_________________________________________________________
#       c) Implement a decision tree for choosing the best match
#_________________________________________________________

total_count = len(LMA_actors)
bvdindex = 0
print total_count, "actors need to be matched"

output_columns = ['LMA_key', 'Name',
                  'Postcode', 'City', 'Street', 'Huisnr',
                  'NACE', 'Role', 'BvDid']

# DECISION 1a: the same BvDid is found matching by name and by address
confirmed_or_unmatched = actors_full_merge[actors_full_merge['BvDid_by_address'] == actors_full_merge['BvDid_by_name']]

confirmed = confirmed_or_unmatched[confirmed_or_unmatched['BvDid_by_address'] != '']
confirmed_count = len(confirmed.index)
print confirmed_count, 'actors have been confirmed'

#output file 1a
confirmed_output = confirmed[['LMA_key', 'Name',
                              'LMA_postcode', 'LMA_plaats', 'LMA_straat', 'LMA_huisnr',
                              'NACE_by_address', 'who', 'BvDid_by_address']]
confirmed_output.columns = output_columns

# DECISION 1b: actor has not been matched neither by name nor address
unmatched = confirmed_or_unmatched[confirmed_or_unmatched['BvDid_by_address'] == '']
unmatched_count = len(unmatched.index)
print unmatched_count, 'actors have been unmatched'

#output file 1b
unmatched_output = unmatched[['LMA_key', 'Name',
                              'LMA_postcode', 'LMA_plaats', 'LMA_straat', 'LMA_huisnr', 'who']]


unmatched_output.reset_index(drop=True, inplace=True)
# unmatched_output['BvDid'] = 'LMA' + scope + unmatched_output.index.map(str).str.zfill(5)
unmatched_output['BvDid'] = unmatched_output.index.map(int)
unmatched_output['BvDid'] = unmatched_output['BvDid'].apply(give_bvdid, scope=scope, start_bvd=bvdindex)
# unmatched_output.set_index('Index', drop=True, inplace=True)
bvdindex += len(unmatched_output.index)

unmatched_output['NACE'] = unmatched_output['who'].apply(give_nace)
unmatched_output = unmatched_output[['LMA_key', 'Name',
                              'LMA_postcode', 'LMA_plaats', 'LMA_straat', 'LMA_huisnr', 'NACE', 'who', 'BvDid']]
unmatched_output.columns = output_columns

# take out those actors that had been confirmed or unmatched
actors_step2 = actors_full_merge[(actors_full_merge['LMA_key'].str.cat(actors_full_merge['who']).isin(confirmed_or_unmatched['LMA_key'].str.cat(confirmed_or_unmatched['who'])) == False)]

# DECISION 2a: actor has been matched to only one BvDid by address, nothing by name
actors_step2['freq'] = actors_step2.groupby(['LMA_key', 'who'])['LMA_key'].transform('count')
single_match = actors_step2[actors_step2['freq'] == 1]

by_address = single_match[single_match['BvDid_by_name'] == '']
by_address_count = len(by_address.index)
print by_address_count, "actors have been matched only by address"

#output file 2a
by_address_output = by_address[['LMA_key', 'Name',
                              'LMA_postcode', 'LMA_plaats', 'LMA_straat', 'LMA_huisnr',
                              'NACE_by_address', 'who']]

by_address_output.reset_index(drop=True, inplace=True)
by_address_output['BvDid'] = by_address_output.index.map(int)
by_address_output['BvDid'] = by_address_output['BvDid'].apply(give_bvdid, scope=scope, start_bvd=bvdindex)
bvdindex += len(by_address_output.index)

by_address_output.columns = output_columns

# DECISION 2b: actor has been matched to only one BvDid by name, nothing by address
by_name = single_match[single_match['BvDid_by_address'] == '']
by_name_count = len(by_name.index)
print by_name_count, "actors have been matched only by name"

#output file 2b
by_name_output = by_name[['LMA_key', 'Name',
                          'LMA_postcode', 'LMA_plaats', 'LMA_straat', 'LMA_huisnr',
                          'NACE_by_name', 'who']]

by_name_output.reset_index(drop=True, inplace=True)
by_name_output['BvDid'] = by_name_output.index.map(int)
by_name_output['BvDid'] = by_name_output['BvDid'].apply(give_bvdid, scope=scope, start_bvd=bvdindex)
bvdindex += len(by_name_output.index)

by_name_output.columns = output_columns

# DECISION 2c: actor has been matched by both name and address but to different actors
by_name_and_address = single_match[(single_match['BvDid_by_name'] != '') & (single_match['BvDid_by_address'] != '')]
by_name_and_address_count = len(by_name_and_address.index)
print by_name_and_address_count, "actors have been matched by name and address to different entities"

by_name_and_address_a = by_name_and_address[by_name_and_address['Year_by_address'] >= by_name_and_address['Year_by_name']]
by_name_and_address_n = by_name_and_address[by_name_and_address['Year_by_address'] < by_name_and_address['Year_by_name']]

#output file 2c
by_a_output = by_name_and_address_a[['LMA_key', 'Name',
                                     'LMA_postcode', 'LMA_plaats', 'LMA_straat', 'LMA_huisnr',
                                     'NACE_by_address', 'who']]
by_n_output = by_name_and_address_n[['LMA_key', 'Name',
                                     'LMA_postcode', 'LMA_plaats', 'LMA_straat', 'LMA_huisnr',
                                     'NACE_by_name', 'who']]

by_a_output.reset_index(drop=True, inplace=True)
by_a_output['BvDid'] = by_a_output.index.map(int)
by_a_output['BvDid'] = by_a_output['BvDid'].apply(give_bvdid, scope=scope, start_bvd=bvdindex)
bvdindex += len(by_a_output.index)

by_n_output.reset_index(drop=True, inplace=True)
by_n_output['BvDid'] = by_n_output.index.map(int)
by_n_output['BvDid'] = by_n_output['BvDid'].apply(give_bvdid, scope=scope, start_bvd=bvdindex)
bvdindex += len(by_n_output.index)

by_a_output.columns = output_columns
by_n_output.columns = output_columns
by_name_and_address_output = pd.concat([by_a_output, by_n_output])


# take out those actors that had been matched
actors_step3 = actors_step2[(actors_step2['freq'] != 1)]

# DECISION 3: actor has been matched to multiple others by name and address

# all possibilities are equal, therefore the dataframe needs to be reorganised vertically
step3_a = actors_step3[['LMA_key', 'Name',
                        'LMA_postcode', 'LMA_plaats', 'LMA_straat', 'LMA_huisnr',
                        'NACE_by_address', 'who', 'BvDid_by_address', 'Year_by_address']]
step3_n = actors_step3[['LMA_key', 'Name',
                        'LMA_postcode', 'LMA_plaats', 'LMA_straat', 'LMA_huisnr',
                        'NACE_by_name', 'who', 'BvDid_by_name', 'Year_by_name']]
step3_n = step3_n[step3_n['BvDid_by_name'] != '']
step3_a.columns = output_columns + ['Year']
step3_n.columns = output_columns + ['Year']

step3 = pd.concat([step3_a, step3_n])
step3.drop_duplicates(inplace=True)
step3['Year'].replace('', '0', inplace=True)
step3['Year'] = step3['Year'].astype(int)
step3.reset_index(drop=True, inplace=True)

ambiguous_match = step3.loc[step3.groupby(['LMA_key', 'Role'])['Year'].idxmax()]
ambiguous_export = pd.merge(actors_step3, ambiguous_match[['LMA_key', 'BvDid']], how='left', on='LMA_key')
ambiguous_export.to_excel('Exports_{0}_part2/actors_matched_ambiguously.xlsx'.format(scope))

print len(ambiguous_match), "have been matched ambiguously"

# output file 3
ambiguous_match_output = ambiguous_match[output_columns]

ambiguous_match_output.reset_index(drop=True, inplace=True)
ambiguous_match_output['BvDid'] = ambiguous_match_output.index.map(int)
ambiguous_match_output['BvDid'] = ambiguous_match_output['BvDid'].apply(give_bvdid, scope=scope, start_bvd=bvdindex)
bvdindex += len(ambiguous_match_output.index)

unconfirmed_output = pd.concat([unmatched_output, by_address_output, by_name_output, by_name_and_address_output, ambiguous_match_output])

# CONSTRAINT 1:
    # ontdoener can have any NACE,
    # inzamelaar can belong to groups E, H, otherwise UNKNOWN
    # ontvanger can belong to groups E, H, otherwise UNKNOWN
    # verwerker can belong to groups E, H, otherwise UNKNOWN
    # exception: an actors has been matched by both name and address

actors_constraint1 = unconfirmed_output[unconfirmed_output['Role'] != 'ontdoener']
actors_constraint1 = actors_constraint1[actors_constraint1['NACE'].str.startswith('E') == False]
actors_constraint1 = actors_constraint1[actors_constraint1['NACE'].str.startswith('H') == False]

actors_no_constraint1 = pd.concat([actors_constraint1, unconfirmed_output]).drop_duplicates(keep=False)

actors_constraint1['NACE'] = actors_constraint1['Role'].apply(give_nace)

all_actors = pd.concat([confirmed_output, actors_no_constraint1, actors_constraint1])

# CONSTRAINT 2: if the same BvDid refers to actors that have different postcodes, then a new BvDid must be given to those actors keeping the same NACE
actors_constraint2 = all_actors.copy()
actors_constraint2['freq_bvd'] = actors_constraint2.groupby('BvDid')['BvDid'].transform('count')
actors_constraint2['freq_pc'] = actors_constraint2.groupby(['BvDid', 'Postcode'])['Postcode'].transform('count')

actors_no_constraint2 = actors_constraint2[actors_constraint2['freq_bvd'] == actors_constraint2['freq_pc']]
actors_constraint2 = actors_constraint2[actors_constraint2['freq_bvd'] != actors_constraint2['freq_pc']]
print len(actors_constraint2), "actors have been mapped to a BvDid that already has a company assigned to a different address"

group_vars = ['BvDid', 'Postcode']
actors_original2 = actors_constraint2.loc[actors_constraint2.groupby('BvDid')['Postcode'].idxmin()]

actors_reidentified = pd.concat([actors_constraint2, actors_original2]).drop_duplicates(keep=False)

actors_reidentified.reset_index(drop=True, inplace=True)
actors_reidentified['BvDid'] = actors_reidentified.index.map(int)
actors_reidentified['BvDid'] = actors_reidentified['BvDid'].apply(give_bvdid, scope=scope, start_bvd=bvdindex)
bvdindex += len(actors_reidentified.index)

actors_cleaned = pd.concat([actors_no_constraint2, actors_original2, actors_reidentified])
actors_cleaned = actors_cleaned[output_columns]

# CONSTRAINT 3: if the same BvDid refers to actors that have different roles, then a new BvDid must be given to those actors keeping the same NACE
actors_constraint3 = actors_cleaned.copy()
actors_constraint3['freq_bvd'] = actors_constraint3.groupby('BvDid')['BvDid'].transform('count')
actors_constraint3['freq_rl'] = actors_constraint3.groupby(['BvDid', 'Role'])['Role'].transform('count')

actors_no_constraint3 = actors_constraint3[actors_constraint3['freq_bvd'] == actors_constraint3['freq_rl']]
actors_constraint3 = actors_constraint3[actors_constraint3['freq_bvd'] != actors_constraint3['freq_rl']]
print len(actors_constraint3), "actors have been mapped to a BvDid that already has a company assigned to a different role"

actors_constraint3['Chain_order'] = actors_constraint3['Role'].apply(chain_order)

group_vars = ['BvDid', 'Chain_order']
actors_original3 = actors_constraint3.loc[actors_constraint3.groupby('BvDid')['Chain_order'].idxmin()]

actors_reidentified = pd.concat([actors_constraint3, actors_original3]).drop_duplicates(keep=False)

actors_reidentified.reset_index(drop=True, inplace=True)
actors_reidentified['BvDid'] = actors_reidentified.index.map(int)
actors_reidentified['BvDid'] = actors_reidentified['BvDid'].apply(give_bvdid, scope=scope, start_bvd=bvdindex)
bvdindex += len(actors_reidentified.index)

actors_matched = pd.concat([actors_no_constraint3, actors_original3, actors_reidentified])
actors_matched = actors_matched[output_columns]

# export the final list of actors

actors_matched.to_excel('Exports_{0}_part2/actors_matched.xlsx'.format(scope))

#_____________________________________________________________________________
#_____________________________________________________________________________
# N E W    A C T O R   T A B L E
#_____________________________________________________________________________
#_____________________________________________________________________________

new_actors = pd.concat([actors_reidentified, unmatched_output])
new_actors.drop_duplicates(subset=['BvDid'], inplace=True)
# the unknown fields are filled with empty cells
new_actors['code'] = ''
new_actors['year'] = 2016
new_actors['description english'] = ''
new_actors['description original'] = ''
new_actors['BvDii'] = ''
new_actors['Website'] = ''
new_actors['employees'] = ''
new_actors['turnover'] = ''
new_actors = new_actors[['BvDid', 'Name', 'code', 'year', 'description english', 'description original',
                         'BvDii', 'Website', 'employees', 'turnover', 'NACE']]

new_actors.to_excel('Exports_{0}_part2/Export_LMA_actors.xlsx'.format(scope))


#_____________________________________________________________________________
#_____________________________________________________________________________
#  A C T O R    L O C A T I O N S    T A B L E
#_____________________________________________________________________________
#_____________________________________________________________________________

locations = actors_matched.copy()
locations['Address'] = locations['Street'].map(str) + ' ' + locations['Huisnr'].map(str)
locations = locations[['BvDid', 'Postcode', 'Address', 'City']]
locations.drop_duplicates(subset=['BvDid', 'Postcode'], inplace=True)

locations.to_excel('Exports_{0}_part2/Export_LMA_actors_locations.xlsx'.format(scope))

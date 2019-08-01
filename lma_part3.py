import os #use to create new folders and change in between different folders

import pandas as pd #python data analysis library

import numpy as np #python scientific computing library

import warnings #ignore unnecessary warnings
warnings.simplefilter(action = 'ignore', category = FutureWarning)
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

# 0.a )  R E A D I N G   F I L E S
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

# choose scope: Food Waste or Construction & Demolition Waste
while True:
    scope = raw_input('Choose scope: CDW or FW\n')
    if scope == 'CDW' or scope == 'FW':
        break
    else:
        print 'Wrong choice.'

Exportfolder = '{0}/LMA data/Exports_{1}_part3'.format(projectname, scope)
if not os.path.exists(Exportfolder): # create folder if it does not exist
    os.makedirs(Exportfolder)

DataFolder = "{0}/LMA data".format(projectname)
os.chdir(DataFolder) # change to Part 1 folder

#_________________________________________________________
# 0.b) M O D E L L I N G   V A R I A B L E S
#_________________________________________________________

# take out variables from the modelling decision input sheet
Modelling_Decisions=pd.read_excel('Interface_data.xlsx') #read

Sensitivity_boundary=Modelling_Decisions.loc[2]['Value'] #set the sensitivity boundary as indicated in the Interface_data file as the boundary
Sensitivity_boundary=float(Sensitivity_boundary)

#_________________________________________________________
 #0.C) Reading in the Comprehensive table from Part 1 and the material correspondance table
 #_________________________________________________________

LMA = pd.read_excel('Exports_{0}_part1/Export_LMA_Analysis_comprehensive_part1.xlsx'.format(scope))
#if manual matching of actors has been made, that file could be used instead of the automatically generated one
while True:
    manual = raw_input('Has a manual matching of actors been made? Y/N\n')
    if manual == 'Y':
        actors_matched = pd.read_excel('Exports_{0}_part2/actors_matched_manually.xlsx'.format(scope))
        break
    elif manual == 'N':
        actors_matched = pd.read_excel('Exports_{0}_part2/actors_matched.xlsx'.format(scope))
        break
    else:
        print 'Wrong choice.'

actors_matched = actors_matched[['LMA_key', 'NACE', 'BvDid', 'Role']]

#read the correspondance table between the EWC code, waste description and GDSE material hierarchy
corresp = pd.read_excel('Exports_{0}_part2/corresp_composition_materials.xlsx'.format(scope))


#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
# 4 ) M E R G I N G   A C T O R S   T O   T H E I R    B V D I D
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________________
# connecting all actors in the flows to their BVDiDs
#_______________________________________________________________________________________________________________________________


roles = ['Ontdoener', 'Inzamelaar', 'Ontvanger', 'Verwerker']

for role in roles:

    postcode = '{0}_Postcode'.format(role)
    if role == 'Ontdoener':
        postcode = 'Postcode'

    LMA[postcode] = LMA[postcode].str.replace(' ','')
    LMA[postcode] = LMA[postcode].str.upper()
    LMA[role] = LMA[role].str.upper()
    LMA[role] = LMA[role].str.replace('BV', '')
    LMA[role] = LMA[role].str.replace('B.V.', '')
    LMA[role] = LMA[role].str.strip()
    LMA[role] = LMA[role].str.upper()

    actors_by_role = actors_matched[actors_matched['Role'] == role.lower()]

    LMA['LMA_key'] = LMA[role] + ' ' + LMA[postcode]
    LMA_merged = pd.merge(LMA, actors_by_role[['LMA_key', 'BvDid']], how='left', on='LMA_key')
    LMA_merged.rename(columns={'BvDid': '{0}_BvDid'.format(role)}, inplace=True)
    LMA = LMA_merged

#_______________________________________________________________________________________________________________________________
# connecting the whole flow to the NACE of the waste producer (herkomst/ontdoener)
#_______________________________________________________________________________________________________________________________

LMA['LMA_key'] = LMA['Ontdoener'] + ' ' + LMA['Postcode']
ontdoeners = actors_matched[actors_matched['Role'] == 'ontdoener']
LMA_merged = pd.merge(LMA, ontdoeners[['LMA_key', 'NACE']], how='left', on='LMA_key')
LMA = LMA_merged



# provide sensitivity data only on non-route entries
LMA_sens_check = LMA[LMA['Route'] == 'JA']

#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
# 5 ) S E N S I T I V I T Y    C H E C K
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

#######
# STEP 5 a
#######

#sensitivity check for NACE code - take extra attention if a NACE code has very few BVDiD entries
LMA_sens_check_nace=LMA_sens_check[['NACE','Ontdoener_BvDid']]
LMA_sens_check_nace['Count']=1
LMA_sens_check_nace_=LMA_sens_check_nace.groupby('NACE')
LMA_sens_check_nace=LMA_sens_check_nace_.aggregate(np.sum).reset_index()
LMA_sens_check_nace.sort_values('Count', ascending=True)
LMA_sens_check_nace.loc[LMA_sens_check_nace['Count']<Sensitivity_boundary, 'Sensitive_NACE']='Yes'
LMA_sens_check_nace.loc[LMA_sens_check_nace['Count']>=Sensitivity_boundary, 'Sensitive_NACE']='No'

#######
# STEP 5 b
#######
#and per postcode - find on how many differeent postcodes a certain Euralcode appears
LMA_sens_check_postcode=LMA_sens_check[['EuralCode','Postcode']]
LMA_sens_check_postcode['Count']=1 #count
LMA_sens_check_postcode_=LMA_sens_check_postcode.groupby('EuralCode') # group all counts together
LMA_sens_check_postcode=LMA_sens_check_postcode_.aggregate(np.sum).reset_index()
LMA_sens_check_postcode.sort_values('Count', ascending=True)
LMA_sens_check_postcode.loc[LMA_sens_check_postcode['Count']<Sensitivity_boundary, 'Sensitive_Postcode']='Yes'
LMA_sens_check_postcode.loc[LMA_sens_check_postcode['Count']>=Sensitivity_boundary, 'Sensitive_Postcode']='No'

#choose either one of these two options
LMA_sens_information_nace=LMA_sens_check_nace.copy()

#add two sensitivity columns - sensitivity on NACE and sensitivity on Postcode
# sensitivity on NACE
LMA_sens_information_nace['NACE']=LMA_sens_information_nace['NACE'].astype(str) #EDIT cleaning data
LMA_sens_information_nace['NACE']=LMA_sens_information_nace['NACE'].str.rstrip('.0') #EDIT cleaning data
LMA_w_BVDid=pd.merge(LMA,LMA_sens_information_nace,on='NACE', how='left')
del LMA_w_BVDid['Count']
LMA_w_BVDid.loc[LMA_w_BVDid['Sensitive_NACE']!='Yes', 'Sensitive_NACE']='No'

# sensitivity on Postcode
LMA_w_BVDid=pd.merge(LMA,LMA_sens_check_postcode,on='EuralCode', how='left')
del LMA_w_BVDid['Count']
LMA_w_BVDid.loc[LMA_w_BVDid['Sensitive_Postcode']!='Yes', 'Sensitive_Postcode']='No'


if scope == 'FW':

    #######
    # STEP 6

    #_________________________________________________________
    #       a) For connecting the fractios of FW according to the 'CBS Voedselverspilling report'
    #_________________________________________________________
    # Reading in the fraction tables from the report
    CBS_FW_fractions=pd.read_excel('CBS_voedselverspilling.xlsx',sheetname='fraction_FW',skiprows=4)
    CBS_FW_fractions.rename(columns={'NACE_code':'NACE lv2'},inplace=True)
    del CBS_FW_fractions['NACE_name']


    #read in document (originally a google doc)
    Afvalbenamingen_EN=pd.read_excel('FW_Eurals_BenamingAfval.xlsx')
    Afvalbenamingen_EN=Afvalbenamingen_EN[['EuralCode','Dutch name','Avoidable (x)']]
    Afvalbenamingen_EN.rename(columns={'Dutch name':'BenamingAfval'},inplace=True)

    # LMA_w_BVDid['NACE']=LMA_w_BVDid['NACE'].convert_objects(convert_numeric=True)
    LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('A'), 'NACE lv2']='No fraction av (agriculture)' #in the CBS document it is stated that they were not able to make any estimation for NACE 3.XX (agriculture)


    if LMA_w_BVDid['NACE'].dtype != np.number:
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-101')==True, 'NACE lv2']=10.1
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-102')==True, 'NACE lv2']=10.2
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-103')==True, 'NACE lv2']=10.3
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-104')==True, 'NACE lv2']=10.4
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-105')==True, 'NACE lv2']=10.5
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-106')==True, 'NACE lv2']=10.6
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-107')==True, 'NACE lv2']=10.7
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-108')==True, 'NACE lv2']=10.8
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-109')==True, 'NACE lv2']=10.9
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-11')==True, 'NACE lv2']=11
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('C-12')==True, 'NACE lv2']=12
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('G-46')==True, 'NACE lv2']=46
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('G-47')==True, 'NACE lv2']=47
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('I-55')==True, 'NACE lv2']=55
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('I-56')==True, 'NACE lv2']=56
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('P-85')==True, 'NACE lv2']='P'
        LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('Q-86')==True, 'NACE lv2']=86

    LMA_w_BVDid['NACE'].replace(np.NaN, 'Not connected to BVDid',inplace=True) # if no NACE code found  - not connected to BVDID
    LMA_w_BVDid['NACE lv2'].replace(np.NaN, 'No fraction av',inplace=True) #for anything that still has no value assigned - there is no fraction available for this NACE


    #split dataframe to apply fractions to merge with the FW fraction data from CBS
    #split in 3 -
    #1) eural codes classified as 9.1
    #2) eural codes classified as 9.1
    #3) all CDW waste

    # merge NACE lvl 2 with CBS NACE lvl 2 fractions
    LMA_w_BVDid=pd.merge(LMA_w_BVDid,CBS_FW_fractions,on='NACE lv2',how='left')

    # 1) 9.1
    LMA_w_BVDid_9_1=LMA_w_BVDid[LMA_w_BVDid['EWC Code']==9.1]
    del LMA_w_BVDid_9_1['09.2 Vegetal wastes']
    LMA_w_BVDid_9_1.rename(columns={'09.1 Animal and mixed food waste':'Fraction'},inplace=True)

    # 2) 9.2
    LMA_w_BVDid_9_2=LMA_w_BVDid[LMA_w_BVDid['EWC Code']==9.2]
    del LMA_w_BVDid_9_2['09.1 Animal and mixed food waste']
    LMA_w_BVDid_9_2.rename(columns={'09.2 Vegetal wastes':'Fraction'},inplace=True)

    # 3) CDW
    LMA_w_BVDid_CDW=LMA_w_BVDid[(LMA_w_BVDid['EWC Code']!=9.2)&(LMA_w_BVDid['EWC Code']!=9.1)]
    del LMA_w_BVDid_CDW['09.1 Animal and mixed food waste']
    del LMA_w_BVDid_CDW['09.2 Vegetal wastes']
    LMA_w_BVDid_CDW['Fraction']='1'

    # connect the the 9.1, 9.2 and CDW dataframes again
    LMA_w_BVDid=pd.concat([LMA_w_BVDid_9_1,LMA_w_BVDid_9_2,LMA_w_BVDid_CDW],ignore_index=True)


    #######
    # STEP 6 b
    #######
    # after manually inspected the waste descriptions, we cound that some of the FW waste descriptions can have a fraction of '1' (i.e. descriptions like 'Swill')
    # and therefore do not need the CBS fractions
    # overwrite this over the existing fractions
    #Afvalbenamingen_EN['EuralCode']=Afvalbenamingen_EN['EuralCode'].astype(str) #EDIT
    LMA_w_BVDid=pd.merge(LMA_w_BVDid,Afvalbenamingen_EN,on=['EuralCode','BenamingAfval'],how='left')  #CHECK THIS - object, object and int and object
    LMA_w_BVDid.loc[LMA_w_BVDid['Avoidable (x)']=='x','Fraction']=1
    del LMA_w_BVDid['Avoidable (x)']

    LMA_w_BVDid.drop_duplicates(inplace=True)

    LMA_w_BVDid['Fraction']=LMA_w_BVDid['Fraction'].replace(np.NaN, '')
    LMA_w_BVDid.loc[LMA_w_BVDid['Fraction']=='','Fraction']=1

elif scope == 'CDW':
    LMA_w_BVDid['Fraction'] = 1


#######
# STEP 7
#######
#add our (english) categorization of the waste treatment process description
WT_descr=pd.read_excel('Preprocessing_description.xlsx')
WT_descr.drop_duplicates(inplace=True)
LMA_w_BVDid = pd.merge(LMA_w_BVDid, WT_descr, on='VerwerkingsOmschrijving', how='left')

#_____________________________________________________________________________
#_____________________________________________________________________________
# P R E P A R I N G   F I L E S    F O R    G D S E
#_____________________________________________________________________________
#_____________________________________________________________________________

LMA_toGDSE=LMA_w_BVDid.copy()
LMA_toGDSE.rename(columns={'MeldPeriodeJAAR': 'Year'}, inplace=True)

#merge correspondance table
LMA_toGDSE['Key'] = LMA_toGDSE['EuralCode'].map(str) + ' ' + LMA_toGDSE['BenamingAfval']
LMA_toGDSE['Key'] = LMA_toGDSE['Key'].str.lower()
LMA_toGDSE['Key'] = LMA_toGDSE['Key'].str.strip()
LMA_toGDSE['Key'] = LMA_toGDSE['Key'].str.replace(u'\xa0', u' ')

#clean the description
corresp['Key'] = corresp['Key'].str.lower()
corresp['Key'] = corresp['Key'].str.strip()
corresp['Key'] = corresp['Key'].str.replace(u'\xa0', u' ')
corresp.drop_duplicates(subset=['Key', 'Material'], inplace=True)
LMA_toGDSE_corresp = pd.merge(LMA_toGDSE, corresp, on='Key', how='left')

LMA_toGDSE_corresp.to_excel('Exports_{0}_part3/Export_LMA_Analysis_comprehensive_part3.xlsx'.format(scope))

#_____________________________________________________________________________
#_____________________________________________________________________________
# C O M P O S I T I O N   T A B L E
#_____________________________________________________________________________
#_____________________________________________________________________________

Composition_table = LMA_toGDSE_corresp[['NACE', 'Key', 'Material', 'Fraction', 'Avoidable', 'Haz']]
Composition_table['Name'] = Composition_table['NACE'] + ' ' + Composition_table['Key']

if scope == 'FW':
    Composition_table['Source'] = 'cbs2017'

    # the fractions in CBS report have been reported for the avoidable parts of the food waste
    # the unavoidable parts need to be calculated
    homogenuous = Composition_table[Composition_table['Fraction']==1]
    avoidable = Composition_table[Composition_table['Fraction']<1]
    avoidable['Avoidable'] = True
    unavoidable = avoidable.copy()
    unavoidable['Fraction'] = 1 - unavoidable['Fraction']
    unavoidable['Avoidable'] = False

    Composition_table = pd.concat([homogenuous, avoidable, unavoidable])
    Composition_table.sort_values(['Name'], inplace=True)

elif scope == 'CDW':
    Composition_table['Source'] = 'lma2018'
    Composition_table['Fraction'] = 1
    Composition_table['Avoidable'] = 'FALSE'

Composition_table['Hazardous'] = np.where(Composition_table['Haz'] == 'Hazardous', True, False)

Composition_table.drop_duplicates(inplace=True)

Composition_table_output = Composition_table[['NACE', 'Name', 'Material', 'Fraction', 'Avoidable', 'Source', 'Hazardous']]


Composition_table_output.to_excel('Exports_{0}_part3/Export_Composition_{0}.xlsx'.format(scope))


#_____________________________________________________________________________
#_____________________________________________________________________________
# F L O W   T A B L E
#_____________________________________________________________________________
#_____________________________________________________________________________


Flow_table = LMA_toGDSE.copy()
Flow_table['Composition'] = Flow_table['NACE'] + ' ' + Flow_table['Key']
Flow_table['Waste'] = True
Flow_table['Source'] = 'lma2018'


#Ontdoener  - Inzamelaar - Ontvanger - Verwerker
Flow_table.replace(np.NaN, '',inplace=True)
Flow_table.loc[Flow_table['Inzamelaar']!='', 'Chain1']='0-1'
Flow_table.loc[Flow_table['Inzamelaar']=='', 'Chain1']='0-2'
Flow_table.loc[(Flow_table['Inzamelaar']=='')&(Flow_table['Ontvanger']==''), 'Chain1']='0-3'
Flow_table.loc[(Flow_table['Chain1']=='0-1')&(Flow_table['Ontvanger']!=''), 'Chain2']='1-2'
Flow_table.loc[(Flow_table['Chain1']=='0-1')&(Flow_table['Ontvanger']==''), 'Chain2']='1-3'
Flow_table.loc[(Flow_table['Chain1']=='0-2')|(Flow_table['Chain2']=='1-2')&(Flow_table['Verwerker']!=''), 'Chain3']='2-3'

Flow_table_herkomst_inzamelaar=Flow_table[Flow_table['Chain1']=='0-1']
Flow_table_herkomst_ontvanger=Flow_table[Flow_table['Chain1']=='0-2']

Flow_table_inzamelaar_ontvanger=Flow_table[Flow_table['Chain2']=='1-2']
Flow_table_inzamelaar_verwerker=Flow_table[Flow_table['Chain2']=='1-3'] #also empty

Flow_table_ontvanger_verwerker=Flow_table[Flow_table['Chain3']=='2-3']

def delete_columns(df):
    del df['Chain1']
    del df['Chain2']
    del df['Chain3']
    return df

Flow_table_herkomst_inzamelaar=delete_columns(Flow_table_herkomst_inzamelaar)
Flow_table_herkomst_ontvanger=delete_columns(Flow_table_herkomst_ontvanger)
Flow_table_inzamelaar_ontvanger=delete_columns(Flow_table_inzamelaar_ontvanger)
Flow_table_inzamelaar_verwerker=delete_columns(Flow_table_inzamelaar_verwerker)
Flow_table_ontvanger_verwerker=delete_columns(Flow_table_ontvanger_verwerker)

output_columns = ['Origin', 'Destination', 'Amount', 'Composition', 'Year', 'Waste', 'Source', 'Description', 'Process']

Flow_table_herkomst_inzamelaar=Flow_table_herkomst_inzamelaar[['Ontdoener_BvDid', 'Inzamelaar_BvDid',
                                                               'Gewicht_KG', 'Composition',
                                                               'Year', 'Waste', 'Source',
                                                               'BenamingAfval', 'Processing description']]

Flow_table_herkomst_inzamelaar.columns = output_columns


Flow_table_herkomst_ontvanger = Flow_table_herkomst_ontvanger[['Ontdoener_BvDid', 'Ontvanger_BvDid',
                                                               'Gewicht_KG', 'Composition',
                                                               'Year', 'Waste', 'Source',
                                                               'BenamingAfval', 'Processing description']]

Flow_table_herkomst_ontvanger.columns = output_columns

Flow_table_inzamelaar_ontvanger = Flow_table_inzamelaar_ontvanger[['Inzamelaar_BvDid', 'Ontvanger_BvDid',
                                                                   'Gewicht_KG', 'Composition',
                                                                   'Year', 'Waste', 'Source',
                                                                   'BenamingAfval', 'Processing description']]

Flow_table_inzamelaar_ontvanger.columns = output_columns

Flow_table_inzamelaar_verwerker = Flow_table_inzamelaar_verwerker[['Inzamelaar_BvDid', 'Verwerker_BvDid',
                                                                   'Gewicht_KG', 'Composition',
                                                                   'Year', 'Waste', 'Source',
                                                                   'BenamingAfval', 'Processing description']]

Flow_table_inzamelaar_verwerker.columns = output_columns

Flow_table_ontvanger_verwerker = Flow_table_ontvanger_verwerker[['Ontvanger_BvDid', 'Verwerker_BvDid',
                                                                 'Gewicht_KG', 'Composition',
                                                                 'Year', 'Waste', 'Source',
                                                                 'BenamingAfval', 'Processing description']]

Flow_table_ontvanger_verwerker.columns = output_columns

Flow_table_output = pd.concat([Flow_table_herkomst_inzamelaar,Flow_table_herkomst_ontvanger,Flow_table_inzamelaar_verwerker,Flow_table_inzamelaar_ontvanger,Flow_table_ontvanger_verwerker],ignore_index=True)

Flow_table_output = Flow_table_output[Flow_table_output['Origin']!=Flow_table_output['Destination']]

# Some of the actors have different names but got matched to the same BvDid (were the same actors)
# That creates duplicate flows (same origin-destination-composition), in that case the flows must be aggregated
Flow_table_output['Amount'] = Flow_table_output.groupby(['Origin', 'Destination', 'Composition'])['Amount'].transform('sum')
Flow_table_output['Amount'] = (Flow_table_output['Amount']/1000).round(0)
Flow_table_output = Flow_table_output[Flow_table_output['Amount']>0]
Flow_table_output.drop_duplicates(inplace=True)

print len(Flow_table_output.index), 'separate flows have been exported'

Flow_table_output.to_excel('Exports_{0}_part3/Export_Flows_{0}.xlsx'.format(scope))

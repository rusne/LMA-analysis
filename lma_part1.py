# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 09:17:31 2018

@author: REPAiR TU Delft Team

"""

# For any questions; you can reach at michelle.steenmeijer or rusne.sileryte
#                                                                   @ gmail.com

import os #use to create new folders and change in between different folders
import pandas as pd #python data analysis library
import numpy as np #python scientific computing library

import warnings #ignore unnecessary warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)
pd.options.mode.chained_assignment = None
#_________________________________________________

#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

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

# 0.b )  C R E A T I N G   F O L D E R S
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

#choose scope: Food Waste or Construction & Demolition Waste
while True:
    scope = raw_input('Choose scope: CDW or FW\n')
    if scope == 'CDW' or scope == 'FW':
        break
    else:
        print 'Wrong choice.'


# LMAfolder=os.path.join(ASMFAfolder,"LMA data") #folder that contains all the needed data
LMAfolder = "{0}/LMA data".format(projectname)
if not os.path.exists(LMAfolder): # create folder if it does not exist
    os.makedirs(LMAfolder)
os.chdir(LMAfolder) #change to LMA folder

# Exportfolder=os.path.join(LMAfolder,"Exports") #Folder where results are sent to
Exportfolder = "Exports_{0}_part1".format(scope)
if not os.path.exists(Exportfolder): # create folder if it does not exist
    os.makedirs(Exportfolder)




#_________________________________________________________
# 0.c) M O D E L L I N G   V A R I A B L E S
#_________________________________________________________


# take out variables from the modelling decision input sheet
Modelling_Decisions=pd.read_excel('Interface_data.xlsx') #read


Year=Modelling_Decisions.loc[0]['Value'] ##set the year as indicated in the Interface_data file as the year of analysis
Ontdoener_location=Modelling_Decisions.loc[1]['Value'] #use this location for the 'Ontdoener' (can be Herkomst, Ontdoener or Afzender)


#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
# 1 a & b )  R E A D I N G   I N    A N D    P R E P A R I N G   T H E    L M A    F I L E S
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
#######
# STEP 1 a
#######


# making a preliminary selection of the columns we want to include in our analysis
LMA_columns = ['Afvalstroomnummer',
               'Ontdoener','Ontdoener_Postcode','Ontdoener_Straat','Ontdoener_Plaats','Ontdoener_Huisnr','Ontdoener_Huisnr.Toevoeging',
               'Herkomst_Postcode','Herkomst_Straat','Herkomst_Plaats','Herkomst_Huisnr','Herkomst_Huisnr.Toevoeging',
               'Afzender','Afzender_Postcode','Afzender_Straat','Afzender_Plaats','Afzender_Huisnummer','Afzender_Huisnr.Toevoeging',           #The Afzender is the one placing the order of picking up the waste
               'Inzamelaar','Inzamelaar_Postcode','Inzamelaar_Straat','Inzamelaar_Plaats','Inzamelaar_Huisnr','Inzamelaar_Huisnr.Toevoeging',
               'Bemiddelaar','Bemiddelaar_Postcode','Bemiddelaar_Straat','Bemiddelaar_Plaats','Bemiddelaar_Huisnr','Bemiddelaar_Huisnr.Toevoeging',
               'Handelaar','Handelaar_Postcode', 'Handelaar_Straat','Handelaar_Plaats','Handelaar_Huisnummer',                                               #can be excluded if necessary
               'Ontvanger','Ontvanger_Postcode', 'Ontvanger_Straat','Ontvanger_Plaats','Ontvanger_Huisnummer',                                               #can be excluded if necessary
               'Verwerker','Verwerker_Postcode','Verwerker_Straat','Verwerker_Plaats','Verwerker_Huisnummer','Verwerker_HuisnummerToevoeging',
               'VerwerkingsmethodeCode','VerwerkingsOmschrijving',
               'RouteInzameling','Inzamelaarsregeling','ToegestaanbijInzamelaarsregeling',
               'EuralCode','EuralcodeOmschrijving','BenamingAfval',
               'MeldPeriodeJAAR','MeldPeriodeMAAND',
               'Gewicht_KG','Aantal_vrachten']

# Reading in the LMA documents

if scope == 'FW':
   LMA = pd.read_excel('Biologisch afbreekbaar afval (Food Waste).xlsx',sheetname='1.OM Ontdoeners in MRA') #using only the '1.OM Ontdoeners in MRA' sheet
elif scope == 'CDW':
   #combine both REPAiR and CINDERELA files into one
   LMA_cinderela = pd.read_excel('20181203 Repair_LMA_Update 28112018_1.xlsx' , sheetname='1.OM Ontdoeners in MRA') #using only the '1.OM Ontdoeners in MRA' sheet
   LMA_cinderela = LMA_cinderela[LMA_columns]
   print 'LMA data for Cinderela has been loaded'

   LMA_repair = pd.read_excel('Bouw- en afvalsloop (CDW).xlsx' , sheetname='1.OM Ontdoeners in MRA')
   LMA_repair = LMA_repair[LMA_columns]
   print 'LMA data for REPAiR has been loaded'

   LMA = pd.concat([LMA_cinderela, LMA_repair])
   combined = len(LMA.index)
   LMA.drop_duplicates(inplace=True)
   cleaned = len(LMA.index)

   print combined - cleaned, 'duplicate lines have been found and removed'
   print 'Final dataset consists of ', cleaned, ' lines'

LMA['Scope'] = scope  # add the scope in a column

#######
# STEP 1 b
#######
#filter LMA data for assigned year
total_AMA = LMA[LMA['MeldPeriodeJAAR'] == Year]

print "Data has been filtered for year {0}".format(Year)




#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
# 1 c)  R E A D I N G   A N D   P R E P A R I N G   A D D I T I O N A L   F I L E S   T O   T H E   L M A   D A T A   F I L E S
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
# INDEX
#######
# STEP 1 c
#######
# subtasks
#       a) For connecting cities (NL: 'Plaats'), with municipalities in order to define which ones are located in the AMA

#       b) For connecting the EuralCode selections and attributes


# EXECUTION

#_________________________________________________________
#       a) For connecting cities (NL: 'Plaats'), with municipalities in order to define which ones are located in the AMA
#_________________________________________________________

# Read in municipality and city data
AMA_cities=pd.read_excel('Cities.xlsx') #sheet with list of Dutch cities and to which municipality they belong
# AMA_mun=pd.read_excel('AMA - spatial classifications.xlsx') #list of municipalities in the AMA

#Transform the Municipality & City data
# to get a list of all Dutch cities, which municipalities they belong to, and whether this municipality belongs to the AMA (Ja/Nee)
# AMA_mun.rename(columns={'Municipality':'Gemeente'}, inplace=True) #rename column name
# AMA_mun['Gemeente']=AMA_mun['Gemeente'].str.upper() #make all letters uppercase
# AMA_cities['Gemeente']=AMA_cities['Gemeente'].str.upper() #make all letters uppercase
# AMA_mun['AMA']='JA'
# AMA_cities['Gemeente']=AMA_cities['Gemeente'].str.upper()#make all letters uppercase
# AMA_cities.rename(columns={'Woonplaats':'Plaats'}, inplace=True)
AMA_cities.rename(columns={'PC4':'Postcode_short', 'In AMA': 'AMA'}, inplace=True)
AMA_cities['Postcode_short'] = AMA_cities['Postcode_short'].apply(str)
# AMA_mun=AMA_mun[['Gemeente','AMA']]
AMA_cities=AMA_cities[['Postcode_short', 'AMA']]
# AMA_cities=pd.merge(AMA_cities,AMA_mun,on='Gemeente',how='left') #merge the list of cities with the list of AMA municipalities to find out which cities are in the AMA
AMA_cities.drop_duplicates(inplace=True) #cleaning data
# AMA_cities['Plaats']=AMA_cities['Plaats'].str.upper()
# AMA_cities=AMA_cities[['Postcode_short', 'Plaats', 'AMA']]
# now AMA_cities is a table with all the Herkomst cities and whether they are in the AMA or not AMA = Ja or empty
# used later

eural = total_AMA['EuralCode']
eural.drop_duplicates(inplace=True)
eural.to_excel("eural.xlsx")

#_________________________________________________________
#       b) For connecting the EuralCode selections and attributes
#_________________________________________________________


# reading in the table with the eural/ewc codes that are related to FW and CDW
Eural_9X = pd.read_excel('EURAL_codes_{0}.xlsx'.format(scope))
Eural_9X.rename(columns={'Eural_code':'EuralCode'},inplace=True)
# data cleaning
Eural_9X['EuralCode'] = Eural_9X['EuralCode'].astype(str)
Eural_9X['EuralCode'] = Eural_9X['EuralCode'].str.replace(' ','')
Eural_9X['EuralCode'] = Eural_9X['EuralCode'].str.replace('*','')
Eural_9X['EuralCode'] = Eural_9X['EuralCode'].astype(int)
total_AMA.replace(np.NaN, '', inplace=True)  # data cleaning step
total_AMA['EuralCode'] = total_AMA['EuralCode'].astype(int)

total_AMA = pd.merge(total_AMA, Eural_9X, on='EuralCode')


print 'After filtering for the relevant EWC codes dataset consists of ', len(total_AMA.index), ' lines'

#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
# 2 - 6)  T R A N S F O R M I N G   T H E   L M A   D A T A   F I L E S   F O R   R E P A i R   A N A L Y S I S
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

#######
# STEP 2
#######
# STEP 2 a
#######

# Add another column 'Route' to add a Ja = Yes, for when Routeverzameling and Inzamelaarsregeling applies (=='J')
#   ! ask whether Inzamelaarsregeling can be regarded as Routeverzameling

total_AMA.loc[(total_AMA['RouteInzameling']=='J')|(total_AMA['Inzamelaarsregeling']=='J'), 'Route' ]='JA' # if for a Afvalstroomnummer the value under Routeinzameling is Inzamelaarsregeling is "J"(=yes), then we assign the value 'JA' for new column 'Route'
total_AMA['Route'].replace(np.NaN,'Nee',inplace=True) #everything that is not Routeverzameling is 'Nee' for column 'Route'


#######
# STEP 2 b
#######
#In order to compare postcodes successfully - we need to make sure all letters in the postcode are either all capitalized or lowercase
total_AMA['Ontdoener_Postcode']=total_AMA['Ontdoener_Postcode'].str.upper() # assigning uppercase method
total_AMA['Herkomst_Postcode']=total_AMA['Herkomst_Postcode'].str.upper()# assigning uppercase method

total_AMA['Herkomst_PC_short']=total_AMA['Herkomst_Postcode'].str[:4]# extracting the numbers from the postcode
total_AMA['Herkomst_Plaats']=total_AMA['Herkomst_Plaats'].str.upper()# assigning uppercase method
total_AMA.replace(np.NaN,'',inplace=True) #data cleaning step

#Since it is possible to report on waste picked up in the AMA (Herkomst) from a company registered in Amsterdam (Ontdoener)
#if the postcodes for Ontdoener and Herkomst are the same OR if the Herkomst field is empty
#   Then the Herkomst location is the same as the Ontdoener location ('JA' in the 'Herkomst-same as ontdoener'-column)
total_AMA.loc[(total_AMA['Ontdoener_Postcode']==total_AMA['Herkomst_Postcode'])|(total_AMA['Herkomst_Postcode']==''), 'Herkomst-same as ontdoener' ]='JA'
total_AMA['Herkomst-same as ontdoener'].replace(np.NaN,'Nee',inplace=True) #everything else is 'Nee'

# Separate data entries for entries with
#   Herkomst is the same as Ontdoener or it is through routeverzameling --> we do not need to check these entries on herkomst (total_AMA_herkomstsame_noroute)
#   Herkomst is NOT the same as Ontdoener & it is not routeverzameling either --> we DO need to check whether entries have Herkomst in the AMA (total_AMA_herkomsNOTsame_route)
total_AMA_herkomstsame_noroute=total_AMA[(total_AMA['Herkomst-same as ontdoener']!='Nee')|(total_AMA['Route']!='Nee')]
total_AMA_herkomsNOTsame_route=total_AMA[(total_AMA['Herkomst-same as ontdoener']=='Nee')&(total_AMA['Route']=='Nee')]

#Find out : from the dataframes that have ontdoeners REGISTERED in the AMA, but herkomst is not the same as the ontdoener location - which herkomst of waste are outside of the AMA? If outside, eliminate
# total_AMA_herkomsNOTsame_route=pd.merge(total_AMA_herkomsNOTsame_route,AMA_cities,on='Herkomst_Plaats',how='left')
total_AMA_herkomsNOTsame_route=pd.merge(total_AMA_herkomsNOTsame_route,AMA_cities,left_on='Herkomst_PC_short', right_on='Postcode_short',how='left')


#data cleaning of city names in the LMA
# total_AMA_herkomsNOTsame_route.loc[total_AMA_herkomsNOTsame_route['Herkomst_Plaats']=='LAREN NH', 'AMA']='JA'
# total_AMA_herkomsNOTsame_route.loc[total_AMA_herkomsNOTsame_route['Herkomst_Plaats']=='AMSTERDAM ZUIDOOST', 'AMA']='JA'

total_AMA_not_generated_in_ama=total_AMA_herkomsNOTsame_route[total_AMA_herkomsNOTsame_route['AMA']!='JA'] # table for the excluded entries, where Herkomst of waste is outside of AMA
total_AMA_herkomstAMA_route=total_AMA_herkomsNOTsame_route[(total_AMA_herkomsNOTsame_route['AMA']=='JA')|(total_AMA_herkomsNOTsame_route['Herkomst_Plaats']=='')] #still include Routeverzameling and where Herkomst of waste is in AMA
del total_AMA_herkomstAMA_route['AMA']

#add the herkomst=same as ondoener, plus route, plus herkomst=AMA together
total_AMA=pd.concat([total_AMA_herkomstsame_noroute,total_AMA_herkomstAMA_route],ignore_index=True)


#######
# STEP 2 c
#######

#Find the aggregated weight per year for each Afvalstroomnummer (as now the waste is reported per month)
total_AMA_agg=total_AMA.copy()
ASN_massa_=total_AMA_agg[['Afvalstroomnummer','Gewicht_KG','Aantal_vrachten']].groupby('Afvalstroomnummer')
ASN_massa=ASN_massa_.aggregate(np.sum).reset_index()
ASN_massa.drop_duplicates(inplace=True)
del total_AMA_agg['MeldPeriodeMAAND']
del total_AMA_agg['Gewicht_KG']
del total_AMA_agg['Aantal_vrachten']
# del total_AMA_agg['MeldPeriodeJAAR']

#add the total waste per year back to each Afvalstroomnummer
total_AMA_agg.drop_duplicates(inplace=True)
total_AMA_agg=pd.merge(total_AMA_agg,ASN_massa,on='Afvalstroomnummer',how='left')

total_flow_chains = len(total_AMA_agg)
print "Data has been aggregated, the total number of flow chains is ", total_flow_chains

# there are four different 'Waste' locations
#   Ontdoener  -  the company that generated the waste
#   Herkomst   -  the actualy location the waste is picked up
#   Afzender   -  the company/responsible to arrange the pick-up

# if waste originates at ontdoener, the 'Herkomst field is empty'
# if the waste originated from elsewhere, herkomst field is filled
# to have the most complete origins of waste, we are going to use the 'Herkomst' field and - if empty (because waste happens at ondoener), then replace empty field with the location of the ontdoener
#for the 'Herkomst' fields that are empty (because the ontdoener location is the same as the herkomst location), put in the Ontdoener location,
total_AMA_agg.loc[total_AMA_agg['Herkomst_Postcode']=='', 'Herkomst_Postcode']=total_AMA_agg['Ontdoener_Postcode']
total_AMA_agg.loc[total_AMA_agg['Herkomst_Huisnr']=='', 'Herkomst_Huisnr']=total_AMA_agg['Ontdoener_Huisnr']
total_AMA_agg.loc[total_AMA_agg['Herkomst_Straat']=='', 'Herkomst_Straat']=total_AMA_agg['Ontdoener_Straat']
total_AMA_agg.loc[total_AMA_agg['Herkomst_Plaats']=='', 'Herkomst_Plaats']=total_AMA_agg['Ontdoener_Plaats']


# for analysis purposes, 3 dataframes are created -
#Total_AMA_GDSE_herkomst    - location = ontdoener/herkomst hybrid
#Total_AMA_GDSE_ontdoener   - location = ontdoener only
#Total_AMA_GDSE_afzender    - location = afzender only

#######
# STEP 2 d
#######

#LOCATION = HERKOMST, ONTDOENER HYBRID
Total_AMA_GDSE_herkomst=total_AMA_agg.copy()
Total_AMA_GDSE_herkomst.rename(columns={'Herkomst_Postcode':'Postcode'},inplace=True)
Total_AMA_GDSE_herkomst.rename(columns={'Herkomst_Huisnr':'Huisnr'},inplace=True)


#LOCATION = ONTDOENER
Total_AMA_GDSE_ontdoener=total_AMA_agg.copy()
Total_AMA_GDSE_ontdoener.rename(columns={'Ontdoener_Postcode':'Postcode'},inplace=True)
Total_AMA_GDSE_ontdoener.rename(columns={'Ontdoener_Huisnr':'Huisnr'},inplace=True)

#LOCATION = AFZENDER
Total_AMA_GDSE_afzender=total_AMA_agg.copy()
Total_AMA_GDSE_afzender.rename(columns={'Afzender_Postcode':'Postcode'},inplace=True)
Total_AMA_GDSE_afzender.rename(columns={'Afzender_Huisnummer':'Huisnr'},inplace=True)
Total_AMA_GDSE_afzender.rename(columns={'Afzender':'Ontdoener'},inplace=True)

#This dataframe only takes the Verwerker information and leaves out the origins for a separate analysis if necessary
# Total_AMA_GDSE_verwerker=total_AMA_agg[['Verwerker','Verwerker_Postcode','Verwerker_Plaats','Verwerker_Huisnummer','Verwerker_HuisnummerToevoeging',
#                                         'VerwerkingsmethodeCode','VerwerkingsOmschrijving','Route','EuralCode','BenamingAfval','Gewicht_KG','VerwerkingsmethodeCode','VerwerkingsOmschrijving']]
# Total_AMA_GDSE_verwerker.rename(columns={'Verwerker_Postcode':'Postcode'},inplace=True)
# Total_AMA_GDSE_verwerker.rename(columns={'Verwerker_Huisnummer':'Huisnr'},inplace=True)


#From the Interface file, default is set on 'Herkomst', it can also be Ontdoener or Afzender
if Ontdoener_location=='Herkomst':
    Total_AMA_GDSE_routeinz_incl=Total_AMA_GDSE_herkomst.copy()
elif Ontdoener_location=='Ontdoener':
    Total_AMA_GDSE_routeinz_incl=Total_AMA_GDSE_ontdoener.copy()
elif Ontdoener_location=='Afzender':
    Total_AMA_GDSE_routeinz_incl=Total_AMA_GDSE_afzender.copy()

Produced_in_AMA = Total_AMA_GDSE_routeinz_incl.copy()


# Finding out which waste generated in the AMA is also treated within the AMA
#first merge 'Verwerker_plaats' with AMA
# Assign Ja in column 'Treated in AMA' if that is the case
# AMA_cities_verwerkers=AMA_cities.copy()
# AMA_cities_verwerkers.rename(columns={'AMA':'Treated in AMA'},inplace=True)
# Total_AMA_GDSE_routeinz_incl['Verwerker_Plaats']=Total_AMA_GDSE_routeinz_incl['Verwerker_Plaats'].str.upper()
# Total_AMA_GDSE_routeinz_incl['Verwerker_PC_short']=Total_AMA_GDSE_routeinz_incl['Verwerker_Postcode'].str[:4]
# Total_AMA_GDSE_routeinz_incl=pd.merge(Total_AMA_GDSE_routeinz_incl,AMA_cities_verwerkers,left_on='Verwerker_PC_short', right_on='Postcode_short',how='left')
# #dataframe for all LMA entries treated in AMA
# treated_in_AMA=Total_AMA_GDSE_routeinz_incl[Total_AMA_GDSE_routeinz_incl['Treated in AMA']=='JA']
#

#######
# STEP 3
#######
# STEP 3 a
#######

# clean the BenamingAfval field for both streams
Produced_in_AMA['BenamingAfval'] = Produced_in_AMA['BenamingAfval'].str.lower()
Produced_in_AMA['BenamingAfval'] = Produced_in_AMA['BenamingAfval'].str.strip()
Produced_in_AMA['BenamingAfval'] = Produced_in_AMA['BenamingAfval'].str.replace(u'\xa0', u' ')

if scope == 'FW':
    # From the latest list, we take out any 'keywords' that describe waste flows only related to garden/landscape maintenance
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('sloopmaaisel', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('snoei', case=False)==True, 'Include?']= 'no'
    # Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('groenafval', case=False)==True, 'Include?']= 'no' # !!!
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('blad', case=False)==True, 'Include?']= 'no'
    # Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('groen ', case=False)==True, 'Include?']= 'no' # !!!
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('tuin', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('zand', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('grond', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('stob', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('plantsoen', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('takken', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('sloot', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('hout', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('boom', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('stam', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('stronk', case=False)==True, 'Include?']= 'no'
    # Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains(' groen', case=False)==True, 'Include?']= 'no' # !!!
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('aanvoer c.t.a.', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('grond', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('bomen', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('gras', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('snippers', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('schoffel', case=False)==True, 'Include?']= 'no'
    # Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('groen', case=False)==True, 'Include?']= 'no' # !!!
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('bos', case=False)==True, 'Include?']= 'no'
    # Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('groen', case=False)==True, 'Include?']= 'no' # !!!
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('tabak', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('schors', case=False)==True, 'Include?']= 'no'
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('kurk', case=False)==True, 'Include?']= 'no'
    # Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('greoen', case=False)==True, 'Include?']= 'no' # !!!
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('Veiling', case=False)==True, 'Include?']= 'no'

# overwrite any description that nonetheless has 'GFT' included
    Produced_in_AMA.loc[Produced_in_AMA['BenamingAfval'].str.contains('gft', case=False)==True, 'Include?']= 'yes'

#  Exclude all the LMA entries that are only referring to garden/landscaping waste
    Produced_in_AMA_include = Produced_in_AMA[Produced_in_AMA['Include?']!='no']
    del Produced_in_AMA_include['Include?']

    print "Data has been filtered for garden/landscape related keywords, remaining number of flow chain is", len(Produced_in_AMA_include.index)

    #rename DataFrame
    comprehensive = Produced_in_AMA_include.copy()

else:
    comprehensive = Produced_in_AMA.copy()


#_____________________________________________________________________________
#_____________________________________________________________________________
# E X P O R T I N G     C O M P R E H E N S I V E    F I L E
#_____________________________________________________________________________
#_____________________________________________________________________________

#######
# STEP 4
#######
# STEP 4 a
#######
#%%
os.chdir(Exportfolder)
comprehensive.to_excel('Export_LMA_Analysis_comprehensive_part1.xlsx', encoding='utf-8')

#_____________________________________________________________________________
#_____________________________________________________________________________
# E X P O R T I N G     A L L    A C T O R S
#_____________________________________________________________________________
#_____________________________________________________________________________
#export all actors participating in flows


herkomst = comprehensive[['Ontdoener','Postcode','Herkomst_Plaats', 'Herkomst_Straat','Huisnr']]
herkomst['who'] = 'ontdoener'
herkomst.columns = ['Name', 'Postcode', 'Plaats', 'Straat', 'Huisnr', 'who']

inzamelaar = comprehensive[['Inzamelaar','Inzamelaar_Postcode', 'Inzamelaar_Plaats','Inzamelaar_Straat', 'Inzamelaar_Huisnr']]
inzamelaar['who'] = 'inzamelaar'
inzamelaar.columns = ['Name', 'Postcode', 'Plaats', 'Straat', 'Huisnr', 'who']

ontvanger = comprehensive[['Ontvanger','Ontvanger_Postcode','Ontvanger_Plaats','Ontvanger_Straat','Ontvanger_Huisnummer']]
ontvanger['who'] = 'ontvanger'
ontvanger.columns = ['Name', 'Postcode', 'Plaats', 'Straat', 'Huisnr', 'who']

verwerker = comprehensive[['Verwerker','Verwerker_Postcode','Verwerker_Plaats','Verwerker_Straat', 'Verwerker_Huisnummer']]
verwerker['who'] = 'verwerker'
verwerker.columns = ['Name', 'Postcode', 'Plaats', 'Straat', 'Huisnr', 'who']

actors = pd.concat([herkomst, inzamelaar, ontvanger, verwerker])

#data cleaning
actors['Postcode'] = actors['Postcode'].str.replace(' ','')
actors['Postcode'] = actors['Postcode'].str.upper()
actors['Name'] = actors['Name'].str.upper()
actors['Name'] = actors['Name'].str.replace('BV', '')
actors['Name'] = actors['Name'].str.replace('B.V.', '')
actors['Name'] = actors['Name'].str.strip()
actors['Name'] = actors['Name'].str.upper()
actors['Plaats'] = actors['Plaats'].str.strip()
actors['Plaats'] = actors['Plaats'].str.upper()
actors['Straat'] = actors['Straat'].str.strip()
actors['Straat'] = actors['Straat'].str.upper()


actors.drop_duplicates(subset=['Name', 'Postcode', 'who'], inplace=True)
actors = actors[actors['Name'] != '']


# find out how many actors have multiple roles within the chain
actor_roles = actors[['Name', 'Postcode', 'who']]
actor_roles['LMA_key'] = actor_roles['Name'] + ' ' + actor_roles['Postcode']
grouped_roles = actor_roles.groupby('LMA_key')
#grouped_roles = grouped_roles['who'].apply(lambda x: ', '.join(x))
grouped_roles = grouped_roles.agg(lambda x: ', '.join(x)).reset_index()

roles = grouped_roles.groupby('who')['LMA_key'].count()
roles.reset_index(name='count')
roles.rename(columns={'LMA_key': 'count'}, inplace=True)
roles.to_excel('actor_roles_summary.xlsx')


actors.to_excel('Export_LMA_actors.xlsx')

actors_without_postcode = actors[actors['Postcode'] == '']
# actors_with_postcode = actors[actors['Postcode'] != '']
#
# actors_with_postcode.to_excel('Export_LMA_actors.xlsx')
if len(actors_without_postcode.index) > 0:
    actors_without_postcode.to_excel('Export_LMA_actors_without_postcode.xlsx')
    print len(actors_without_postcode.index), 'actors do not have a postcode'
else:
    print 'All actors have a postcode'

# export actors already prepared for the ORBIS batch search
if not os.path.exists('ORBIS_batch_search'): # create folder if it does not exist
    os.makedirs('ORBIS_batch_search')

actors_batch = actors[['Name', 'Plaats']]
actors_batch['Land'] = 'Netherlands'
actors_batch.drop_duplicates(subset=['Name'], inplace=True)
# limitation: multiple companies with the same name could also be located in different cities
# assumption to be checked - a company with the same name in a different address should have still the same NACE code
count = len(actors_batch.index)
slices = range(0, count, 1000) + [count]
for i in range(len(slices) - 1):
    start = slices[i]
    end = slices[i + 1]
    actors_batch[start:end].to_excel('ORBIS_batch_search/LMA_{0}_{1}.xlsx'.format(scope, end), index = False)

print count, "actors have to be searched in ORBIS database"


#_____________________________________________________________________________
#_____________________________________________________________________________
# E X P O R T I N G     A L L    C O M P O S I T I O N S
#_____________________________________________________________________________
#_____________________________________________________________________________
#export all compositions that need to be matched with the material hierarchy

compositions = comprehensive[['EuralCode', 'BenamingAfval']]
compositions.drop_duplicates(inplace=True)
compositions.to_excel('Export_LMA_compositions.xlsx')




print "Comprehensive table, actors and compositions have been exported"

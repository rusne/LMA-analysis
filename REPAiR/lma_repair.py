# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 09:17:31 2018

@author: REPAiR TU Delft Team

"""
#____________START______READ_ME__________________________________
# R E A D   ME - HOW TO RUN THIS SCRIPT

# 1) Run the file as it is now (press F5)
# 2) Download all the xlsx files from the drive folder REPAiR (TUD shared folder) > Data > Data AMA > LMA > Data Folder
# 3) Then, in the newly created 'LMA data' folder in your directory, put here all the xlsx files from the Drive LMA Data folder you just downloaded
# 4) Also add in the LMA files if you have the permission
# 6) run file (press F5)
# 7) Find export results in 'Export' folder that is within your LMA folder
# 8) For any questions; you can reach me at michelle.steenmeijer@gmail.com

#______________________READ_ME________END________________________


#_________________________________________________
import os #use to create new folders and change in between different folders

import pandas as pd #python data analysis library

import numpy as np #python scientific computing library

import warnings #ignore unnecessary warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)
pd.options.mode.chained_assignment = None
#_________________________________________________


#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

# 0.a )  C R E A T I N G   F O L D E R S
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________

#my_dir1=os.path.expanduser('~/Documents') #find the documents folder, assuming your PC has one (change '\\' to '/' if you own a macbook)
#os.chdir(my_dir1)

#ASMFAfolder=os.path.join(my_dir1,"AS-MFA") #projectfolder
# ASMFAfolder = "AS-MFA"
# if not os.path.exists(ASMFAfolder): # create folder if it does not exist
#     os.makedirs(ASMFAfolder)
# os.chdir(ASMFAfolder)



# LMAfolder=os.path.join(ASMFAfolder,"LMA data") #folder that contains all the needed data
LMAfolder = "LMA data"
if not os.path.exists(LMAfolder): # create folder if it does not exist
    os.makedirs(LMAfolder)
os.chdir(LMAfolder) #change to LMA folder

# Exportfolder=os.path.join(LMAfolder,"Exports") #Folder where results are sent to
Exportfolder = "Exports"
if not os.path.exists(Exportfolder): # create folder if it does not exist
    os.makedirs(Exportfolder)




#_________________________________________________________
# 0.b) M O D E L L I N G   V A R I A B L E S
#_________________________________________________________

# take out variables from the modelling decision input sheet
Modelling_Decisions=pd.read_excel('Interface_data.xlsx') #read


Year=Modelling_Decisions.loc[0]['Value'] ##set the year as indicated in the Interface_data file as the year of analysis
Ontdoener_location=Modelling_Decisions.loc[1]['Value'] #use this location for the 'Ontdoener' (can be Herkomst, Ontdoener or Afzender)

Sensitivity_boundary=Modelling_Decisions.loc[2]['Value'] #set the sensitivity boundary as indicated in the Interface_data file as the boundary
Sensitivity_boundary=float(Sensitivity_boundary)


#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
# 1 a & b )  R E A D I N G   I N    A N D    P R E P A R I N G   T H E    L M A    F I L E S
#________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________
#######
# STEP 1 a
#######
 # Reading in the LMA documents
#reading in Food waste LMA data
FW_AMA=pd.read_excel('Biologisch afbreekbaar afval (Food Waste).xlsx',sheetname='1.OM Ontdoeners in MRA') #using only the '1.OM Ontdoeners in MRA' sheet
FW_AMA['Scope']='FW' #add the scope in a column (=food waste/FW)

#reading in Construction and Demolition Waste (CDW) LMA data
CDW_AMA=pd.read_excel('Bouw- en afvalsloop (CDW).xlsx' , sheetname='1.OM Ontdoeners in MRA') #using only the '1.OM Ontdoeners in MRA' sheet
CDW_AMA['Scope']='CDW' #add the name of the scope in a column

#combine both the CDW and FW data
total_AMA=pd.concat([FW_AMA,CDW_AMA],ignore_index=True)

# making a preliminary selection of the columns we want to include in our analysis
total_AMA=total_AMA[['Scope','Afvalstroomnummer',
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
               'Gewicht_KG','Aantal_vrachten']]

#######
# STEP 1 b
#######
#filter LMA data for assigned year
total_AMA=total_AMA[total_AMA['MeldPeriodeJAAR']==Year]




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

#       b) For connecting the LMA database with the Orbis exports for CDW and FW

#       c) For connecting the EuralCode selections and attribites

#       d) For connecting the fractios of FW according to the 'CBS Voedeselverspilling report'

#       e) For deleting manually detected non-FW or non-CDW entries according to the more specific waste description according to the LMA ('AfvalBenaming')



# EXECUTION

#_________________________________________________________
#       a) For connecting cities (NL: 'Plaats'), with municipalities in order to define which ones are located in the AMA
#_________________________________________________________

# Read in municipality and city data
AMA_cities=pd.read_excel('Cities.xlsx') #sheet with list of Dutch cities and to which municipality they belong
AMA_mun=pd.read_excel('AMA - spatial classifications.xlsx') #list of municipalities in the AMA

#Transform the Municipality & City data
# to get a list of all Dutch cities, which municipalities they belong to, and whether this municipality belongs to the AMA (Ja/Nee)
AMA_mun.rename(columns={'Municipality':'Gemeente'}, inplace=True) #rename column name
AMA_mun['Gemeente']=AMA_mun['Gemeente'].str.upper() #make all letters uppercase
AMA_cities['Gemeente']=AMA_cities['Gemeente'].str.upper() #make all letters uppercase
AMA_mun['AMA']='Ja'
AMA_cities['Gemeente']=AMA_cities['Gemeente'].str.upper()#make all letters uppercase
AMA_cities.rename(columns={'Woonplaats':'Herkomst_Plaats'}, inplace=True)
AMA_mun=AMA_mun[['Gemeente','AMA']]
AMA_cities=AMA_cities[['Gemeente','Herkomst_Plaats']]
AMA_cities=pd.merge(AMA_cities,AMA_mun,on='Gemeente',how='left') #merge the list of cities with the list of AMA municipalities to find out which cities are in the AMA
AMA_cities.drop_duplicates(inplace=True) #cleaning data
AMA_cities['Herkomst_Plaats']=AMA_cities['Herkomst_Plaats'].str.upper()
AMA_cities=AMA_cities[['Herkomst_Plaats','AMA']]
# now AMA_cities is a table with all the Herkomst cities and whether they are in the AMA or not AMA = Ja or empty
# used later


#_________________________________________________________
#       b) For connecting the LMA database with the Orbis exports for CDW and FW
#_________________________________________________________


# read in all FW/CDW files
# Since we want to connect the Orbis file with the LMA data based on Postcode and Huisnummer, it is necessary to isolate the Huisnummer from the address line in Orbis
# The following are Orbis files for which the column with the address is prepared with the following:
#treated with - DATA - TEXT TO COLUMN - DELIMITER = 'SPACE' - make sure the address column is the outer right one, so it does not replace other values when address is parsed

#reading in the FW Actors Orbis data
# FW_parsed=pd.read_excel('Orbis_exports_FW_allAG_parsed_address.xlsx')
FW_parsed = pd.read_excel('ORBIS_address_FW.xlsx')
FW_parsed['Scope']='FW'

#reading in the CDW Actors Orbis data
# CDW_D_parsed=pd.read_excel('AMA_CDW_D_parsed_address.xlsx', sheetname='Results') # AMA CDW Orbis entries for Activity Group D
# CDW_D_parsed['Scope']='CDW'
# CDW_WM_parsed=pd.read_excel('AMA_CDW_WM_parsed_address.xlsx', sheetname='Results') # AMA CDW Orbis entries for Activity Group WM
# CDW_WM_parsed['Scope']='CDW'
# CDW_C_parsed=pd.read_excel('AMA_CDW_C_parsed_address.xlsx', sheetname='Results') # AMA CDW Orbis entries for Activity Group C
# CDW_C_parsed['Scope']='CDW'
CDW_parsed = pd.read_excel('ORBIS_address_CDW.xlsx')
CDW_parsed['Scope'] = 'CDW'

#rename the unnamed columns (created with the parsing of the address line)
# CDW_C_parsed.rename(columns={'Unnamed: 40':'Add. column 1'},inplace=True)
# CDW_C_parsed.rename(columns={'Unnamed: 41':'Add. column 2'},inplace=True)
# CDW_WM_parsed.rename(columns={'Unnamed: 53':'Add. column 1'},inplace=True)
# CDW_WM_parsed.rename(columns={'Unnamed: 54':'Add. column 2'},inplace=True)
# FW_parsed.rename(columns={'Unnamed: 28':'Add. column 1'},inplace=True)
# FW_parsed.rename(columns={'Unnamed: 29':'Add. column 2'},inplace=True)

# concatenate all the entries from the four different Orbis files together
# FW_CDW_parsed=pd.concat([FW_parsed,CDW_D_parsed,CDW_C_parsed,CDW_WM_parsed],ignore_index=True)
# FW_CDW_parsed.rename(columns={'Last\navail.\nyear':'Year_orbis','NACE Rev. 2\nCore code (4 digits)':'NACE'}, inplace=True)
# FW_CDW_parsed=FW_CDW_parsed[['Scope','Company name','Postcode','BvD ID number','Year_orbis','NACE','Street,','no.,','building','etc,','line',1,'Add. column 1','Add. column 2']]
FW_CDW_parsed = pd.concat([FW_parsed, CDW_parsed], ignore_index=True)
FW_CDW_parsed=FW_CDW_parsed[['Scope','name','Postcode','BvDid','NACE','City','huisnummer']]


#converting all the parsed columns from the address line into strings so it is possible to detect which parsed column holds the addres number
# FW_CDW_parsed['Street,']=FW_CDW_parsed['Street,'].astype(str)
# FW_CDW_parsed['no.,']=FW_CDW_parsed['no.,'].astype(str)
# FW_CDW_parsed['building']=FW_CDW_parsed['building'].astype(str)
# FW_CDW_parsed['etc,']=FW_CDW_parsed['etc,'].astype(str)
# FW_CDW_parsed['line']=FW_CDW_parsed['line'].astype(str)
# FW_CDW_parsed[1]=FW_CDW_parsed[1].astype(str)
# FW_CDW_parsed['Add. column 1']=FW_CDW_parsed['Add. column 1'].astype(str)

# of the second of the parsed columns can be converted into a digit, then the address line has 'one word'  and the second column can be named Huisnummer.
# if the second of the parsed columns cannot be converted into digits, then add the line to the 'rest' for further analysis
# oneword=FW_CDW_parsed[FW_CDW_parsed['no.,'].str.isdigit()==True]
# rest1=FW_CDW_parsed[FW_CDW_parsed['no.,'].str.isdigit()==False]
# oneword=oneword[['Scope','Company name','Postcode','Year_orbis','NACE','BvD ID number','no.,']]
# oneword.rename(columns={'no.,':'Herkomst_Huisnr'},inplace=True)

# of the third of the parsed columns can be converted into a digit, then the address line has 'two words'  and the third column can be named Huisnummer.
# if the third of the parsed columns cannot be converted into digits, then add the line to the 'rest' for further analysis
# twoword=rest1[rest1['building'].str.isdigit()==True]
# rest2=rest1[rest1['building'].str.isdigit()==False]
# twoword=twoword[['Scope','Company name','Postcode','Year_orbis','NACE','BvD ID number','building']]
# twoword.rename(columns={'building':'Herkomst_Huisnr'},inplace=True)

#etc..
# threeword=rest2[rest2['etc,'].str.isdigit()==True]
# rest3=rest2[rest2['etc,'].str.isdigit()==False]
# threeword=threeword[['Scope','Company name','Postcode','Year_orbis','NACE','BvD ID number','etc,']]
# threeword.rename(columns={'etc,':'Herkomst_Huisnr'},inplace=True)

#etc..
# fourword=rest3[rest3['line'].str.isdigit()==True]
# rest4=rest3[rest3['line'].str.isdigit()==False]
# fourword=fourword[['Scope','Company name','Postcode','Year_orbis','NACE','BvD ID number','line']]
# fourword.rename(columns={'line':'Herkomst_Huisnr'},inplace=True)

#etc..
# fiveword=rest4[rest4[1].str.isdigit()==True]
# rest5=rest4[rest4[1].str.isdigit()==False]
# fiveword=fiveword[['Scope','Company name','Postcode','Year_orbis','NACE','BvD ID number',1]]
# fiveword.rename(columns={1:'Herkomst_Huisnr'},inplace=True)

#etc..
# sixword=rest5[rest5['Add. column 1'].str.isdigit()==True]
# rest6=rest5[rest5['Add. column 1'].str.isdigit()==False]
# sixword=sixword[['Scope','Company name','Postcode','Year_orbis','NACE','BvD ID number','Add. column 1']]
# sixword.rename(columns={'Add. column 1':'Herkomst_Huisnr'},inplace=True)

#etc..
# sevenword=rest6[rest6['Add. column 2'].str.isdigit()==True]
# rest7=rest6[rest6['Add. column 2'].str.isdigit()==False]
# sevenword=sevenword[['Scope','Company name','Postcode','Year_orbis','NACE','BvD ID number','Add. column 2']]
# sevenword.rename(columns={'Add. column 2':'Herkomst_Huisnr'},inplace=True)

#now we can combine all the dataframes for which we identified the Huisnummer together
# all_combinations=pd.concat([oneword, twoword,threeword,fourword,fiveword,sixword,sevenword],ignore_index=True)
# all_combinations.drop_duplicates(inplace=True)

#data cleaning
# all_combinations['Postcode']=all_combinations['Postcode'].str.replace(' ','')
# all_combinations['Postcode']=all_combinations['Postcode'].str.upper()
FW_CDW_parsed['Postcode']=FW_CDW_parsed['Postcode'].str.replace(' ','')
FW_CDW_parsed['Postcode']=FW_CDW_parsed['Postcode'].str.upper()

#take entry of postcode and huisnummer with latest registered BVDid
# BVDid_NACE_postcode_huisnr=all_combinations.loc[all_combinations.groupby(['Postcode','Herkomst_Huisnr'])['Year_orbis'].idxmax()]
# BVDid_NACE_postcode_huisnr.rename(columns={'Herkomst_Huisnr':'Huisnr'},inplace=True)
BVDid_NACE_postcode_huisnr = FW_CDW_parsed
BVDid_NACE_postcode_huisnr.rename(columns={'huisnummer':'Huisnr'},inplace=True)

# take out any entries that do not have any house number at all
BVDid_NACE_postcode_huisnr['Huisnr'].replace(np.NaN,999999,inplace=True)
BVDid_NACE_postcode_huisnr=BVDid_NACE_postcode_huisnr[BVDid_NACE_postcode_huisnr['Huisnr']!=999999] #filter out the entries that do not have a housenumber assigned

# data cleaning
BVDid_NACE_postcode_huisnr['Huisnr']=BVDid_NACE_postcode_huisnr['Huisnr'].astype(int)
BVDid_NACE_postcode_huisnr=BVDid_NACE_postcode_huisnr.drop_duplicates()
BVDid_NACE_postcode_huisnr=BVDid_NACE_postcode_huisnr.reset_index() #EDITED
del BVDid_NACE_postcode_huisnr['index'] #EDITED


#_________________________________________________________
#       c) For connecting the EuralCode selections and attributes
#_________________________________________________________
# reading in the table with the eural/ewc codes that are related to FW and CDW
Eural_9X=pd.read_excel('EURAL_codes_FW_CDW.xlsx')
Eural_9X.rename(columns={'Eural_code':'EuralCode'},inplace=True)
# data cleaning
Eural_9X['EuralCode']=Eural_9X['EuralCode'].astype(str)
Eural_9X['EuralCode']=Eural_9X['EuralCode'].str.replace(' ','')
Eural_9X['EuralCode']=Eural_9X['EuralCode'].str.replace('*','')
Eural_9X['EuralCode']=Eural_9X['EuralCode'].astype(int)

#_________________________________________________________
#       d) For connecting the fractios of FW according to the 'CBS Voedeselverspilling report'
#_________________________________________________________
# Reading in the fraction tables from the report
CBS_FW_fractions=pd.read_excel('CBS_voedselverspilling.xlsx',sheetname='fraction_FW',skiprows=4)
CBS_FW_fractions.rename(columns={'NACE_code':'NACE lv2'},inplace=True)
del CBS_FW_fractions['NACE_name']


#_________________________________________________________
#       e) For deleting manually detected non-FW or non-CDW entries according to the more specific waste description according to the LMA ('AfvalBenaming')
#_________________________________________________________

#read in document (originally a google doc)
Afvalbenamingen_EN=pd.read_excel('FW_Eurals_BenamingAfval_EN.xlsx')
Afvalbenamingen_EN=Afvalbenamingen_EN[['EuralCode','Dutch name','English name','Avoidable (x)']]
Afvalbenamingen_EN.rename(columns={'Dutch name':'BenamingAfval'},inplace=True)
Afvalbenamingen_EN.rename(columns={'English name':'Waste description'},inplace=True)


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
total_AMA.replace(np.NaN, '',inplace=True) # data cleaning step
total_AMA.loc[(total_AMA['RouteInzameling']=='J')|(total_AMA['Inzamelaarsregeling']=='J'), 'Route' ]='Ja' # if for a Afvalstroomnummer the value under Routeinzameling is Inzamelaarsregeling is "J"(=yes), then we assign the value 'Ja' for new column 'Route'
total_AMA['Route'].replace(np.NaN,'Nee',inplace=True) #everything that is not Routeverzameling is 'Nee' for column 'Route'


#######
# STEP 2 b
#######
#In order to compare postcodes successfully - we need to make sure all letters in the postcode are either all capitalized or lowercase
total_AMA['Ontdoener_Postcode']=total_AMA['Ontdoener_Postcode'].str.upper() # assigning uppercase method
total_AMA['Herkomst_Postcode']=total_AMA['Herkomst_Postcode'].str.upper()# assigning uppercase method
total_AMA['Herkomst_Plaats']=total_AMA['Herkomst_Plaats'].str.upper()# assigning uppercase method
total_AMA.replace(np.NaN,'',inplace=True) #data cleaning step

#Since it is possible to report on waste picked up in the AMA (Herkomst) from a company registered in Amsterdam (Ontdoener)
#if the postcodes for Ontdoener and Herkomst are the same OR if the Herkomst field is empty
#   Then the Herkomst location is the same as the Ontdoener location ('Ja' in the 'Herkomst-same as ontdoener'-column)
total_AMA.loc[(total_AMA['Ontdoener_Postcode']==total_AMA['Herkomst_Postcode'])|(total_AMA['Herkomst_Postcode']==''), 'Herkomst-same as ontdoener' ]='Ja'
total_AMA['Herkomst-same as ontdoener'].replace(np.NaN,'Nee',inplace=True) #everything else is 'Nee'

# Separate data entries for entries with
#   Herkomst is the same as Ontdoener or it is through routeverzameling --> we do not need to check these entries on herkomst (total_AMA_herkomstsame_noroute)
#   Herkomst is the NOT same as Ontdoener & it is not routeverzameling either --> we DO need to check whether entries have Herkomst in the AMA (total_AMA_herkomsNOTsame_route)
total_AMA_herkomstsame_noroute=total_AMA[(total_AMA['Herkomst-same as ontdoener']!='Nee')|(total_AMA['Route']!='Nee')]
total_AMA_herkomsNOTsame_route=total_AMA[(total_AMA['Herkomst-same as ontdoener']=='Nee')&(total_AMA['Route']=='Nee')]

#Find out : from the dataframes that have ontdoeners REGISTERED in the AMA, but herkomst is not the same as the ontdoener location - which herkomst of waste are outside of the AMA? If outside, eliminate
total_AMA_herkomsNOTsame_route=pd.merge(total_AMA_herkomsNOTsame_route,AMA_cities,on='Herkomst_Plaats',how='left')

#data cleaning of city names in the LMA
total_AMA_herkomsNOTsame_route.loc[total_AMA_herkomsNOTsame_route['Herkomst_Plaats']=='LAREN NH', 'AMA']='Ja'
total_AMA_herkomsNOTsame_route.loc[total_AMA_herkomsNOTsame_route['Herkomst_Plaats']=='AMSTERDAM ZUIDOOST', 'AMA']='Ja'

total_AMA_not_generated_in_ama=total_AMA_herkomsNOTsame_route[total_AMA_herkomsNOTsame_route['AMA']!='Ja'] # table for the excluded entries, where Herkomst of waste is outside of AMA
total_AMA_herkomstAMA_route=total_AMA_herkomsNOTsame_route[(total_AMA_herkomsNOTsame_route['AMA']=='Ja')|(total_AMA_herkomsNOTsame_route['Herkomst_Plaats']=='')] #still include Routeverzameling and where Herkomst of waste is in AMA
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
del total_AMA_agg['MeldPeriodeJAAR']

#add the total waste per year back to each Afvalstroomnummer
total_AMA_agg.drop_duplicates(inplace=True)
total_AMA_agg=pd.merge(total_AMA_agg,ASN_massa,on='Afvalstroomnummer',how='left')

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
#Total_AMA_GDSE_herkomst    - location = ontdoener/herkomst hydrid
#Total_AMA_GDSE_ontdoener   - location = ontdoener only
#Total_AMA_GDSE_afzender    - location = afzender only

#######
# STEP 2 d
#######

#LOCATION = HERKOMST, ONTDOENER HYBRID
"""
#For a specific set of columns
Total_AMA_GDSE_herkomst=total_AMA_agg[['Scope','Ontdoener',
                              'Herkomst_Postcode','Herkomst_Plaats','Herkomst_Huisnr','Herkomst_Huisnr.Toevoeging', #line of interest
                              'Inzamelaar','Inzamelaar_Postcode','Inzamelaar_Plaats','Inzamelaar_Huisnr','Inzamelaar_Huisnr.Toevoeging',
                              'Verwerker','Verwerker_Postcode','Verwerker_Plaats','Verwerker_HuisnummerToevoeging','Verwerker_Huisnummer',
                              'VerwerkingsmethodeCode','VerwerkingsOmschrijving',
                              'Route',
                              'EuralCode','BenamingAfval',
                              'Gewicht_KG']]
Total_AMA_GDSE_herkomst.rename(columns={'Herkomst_Postcode':'Postcode'},inplace=True)
Total_AMA_GDSE_herkomst.rename(columns={'Herkomst_Huisnr':'Huisnr'},inplace=True)
"""
#For using all columns
Total_AMA_GDSE_herkomst=total_AMA_agg.copy()
Total_AMA_GDSE_herkomst.rename(columns={'Herkomst_Postcode':'Postcode'},inplace=True)
Total_AMA_GDSE_herkomst.rename(columns={'Herkomst_Huisnr':'Huisnr'},inplace=True)


#LOCATION = ONTDOENER
"""
#For a specific set of columns
Total_AMA_GDSE_ontdoener=total_AMA_agg[['Scope','Ontdoener',
                              'Ontdoener_Postcode','Ontdoener_Plaats','Ontdoener_Huisnr','Ontdoener_Huisnr.Toevoeging', #line of interest
                              'Inzamelaar','Inzamelaar_Postcode','Inzamelaar_Plaats','Inzamelaar_Huisnr','Inzamelaar_Huisnr.Toevoeging',
                              'Verwerker','Verwerker_Postcode','Verwerker_Plaats','Verwerker_HuisnummerToevoeging',
                              'VerwerkingsmethodeCode','VerwerkingsOmschrijving',
                              'Route',
                              'EuralCode','BenamingAfval',
                              'Gewicht_KG']]
"""
#For using all columns
Total_AMA_GDSE_ontdoener=total_AMA_agg.copy()
Total_AMA_GDSE_ontdoener.rename(columns={'Ontdoener_Postcode':'Postcode'},inplace=True)
Total_AMA_GDSE_ontdoener.rename(columns={'Ontdoener_Huisnr':'Huisnr'},inplace=True)

#LOCATION = AFZENDER
"""
Total_AMA_GDSE_afzender=total_AMA_agg[['Scope','Afzender',
                              'Afzender_Postcode','Afzender_Plaats','Afzender_Huisnummer','Afzender_Huisnr.Toevoeging', #line of interest
                              'Inzamelaar','Inzamelaar_Postcode','Inzamelaar_Plaats','Inzamelaar_Huisnr','Inzamelaar_Huisnr.Toevoeging',
                              'Verwerker','Verwerker_Postcode','Verwerker_Plaats','Verwerker_HuisnummerToevoeging',
                              'VerwerkingsmethodeCode','VerwerkingsOmschrijving',
                              'Route',
                              'EuralCode','BenamingAfval',
                              'Gewicht_KG']]
"""
#For using all columns
Total_AMA_GDSE_afzender=total_AMA_agg.copy()
Total_AMA_GDSE_afzender.rename(columns={'Afzender_Postcode':'Postcode'},inplace=True)
Total_AMA_GDSE_afzender.rename(columns={'Afzender_Huisnummer':'Huisnr'},inplace=True)
Total_AMA_GDSE_afzender.rename(columns={'Afzender':'Ontdoener'},inplace=True)

#This dataframe only takes the Verwerker information and leaves out the origins for a separate analysis if necessary
Total_AMA_GDSE_verwerker=total_AMA_agg[['Verwerker','Verwerker_Postcode','Verwerker_Plaats','Verwerker_Huisnummer','Verwerker_HuisnummerToevoeging',
                                        'VerwerkingsmethodeCode','VerwerkingsOmschrijving','Route','EuralCode','BenamingAfval','Gewicht_KG','VerwerkingsmethodeCode','VerwerkingsOmschrijving']]
Total_AMA_GDSE_verwerker.rename(columns={'Verwerker_Postcode':'Postcode'},inplace=True)
Total_AMA_GDSE_verwerker.rename(columns={'Verwerker_Huisnummer':'Huisnr'},inplace=True)


#From the Interface file, default is set on 'Herkomst', it can also be Ontdoener or Afzender
if Ontdoener_location=='Herkomst':
    Total_AMA_GDSE_routeinz_incl=Total_AMA_GDSE_herkomst.copy()
elif Ontdoener_location=='Ontdoener':
    Total_AMA_GDSE_routeinz_incl=Total_AMA_GDSE_ontdoener.copy()
else:
#if Ontdoener_location=='Afzender':
    Total_AMA_GDSE_routeinz_incl=Total_AMA_GDSE_afzender.copy()


# Finding out which waste generated in the AMA is also treated within the AMA
#first merge 'Verwerker_plaats' with AMA
# Assign Ja in column 'Treated in AMA' if that is the case
AMA_cities_verwerkers=AMA_cities.copy()
AMA_cities_verwerkers.rename(columns={'Herkomst_Plaats':'Verwerker_Plaats','AMA':'Treated in AMA'},inplace=True)
Total_AMA_GDSE_routeinz_incl['Verwerker_Plaats']=Total_AMA_GDSE_routeinz_incl['Verwerker_Plaats'].str.upper()
Total_AMA_GDSE_routeinz_incl=pd.merge(Total_AMA_GDSE_routeinz_incl,AMA_cities_verwerkers,on='Verwerker_Plaats',how='left')
#dataframe for all LMA entries treated in AMA
treatedinAMA=Total_AMA_GDSE_routeinz_incl[Total_AMA_GDSE_routeinz_incl['Treated in AMA']=='Ja']


#######
# STEP 3
#######
# STEP 3 a
#######

# Merge LMA data with the Orbis export to connect the postcode, huisnummers (and scope) with a BVDid to eventually get a NACE code per waste entry
Total_AMA_GDSE_routeinz_incl['Huisnr'] = pd.to_numeric(Total_AMA_GDSE_routeinz_incl['Huisnr'], errors='coerce') #making sure the datatypes for Huisnummer is the same for the two merged dataframes
LMA_Orbis_merge=pd.merge(Total_AMA_GDSE_routeinz_incl,BVDid_NACE_postcode_huisnr,on=['Postcode','Huisnr','Scope'],how='left') # if you take out scope, there are about 4000 more matches
LMA_Orbis_merge.replace(np.NaN, '',inplace=True) #data cleaning


#######
# STEP 3 b
#######

# Find out which entries did not merge with Orbis data
LMA_Orbis_nomerge=LMA_Orbis_merge[LMA_Orbis_merge['BvDid']==''] #filter
# most that are unmerged are companies that are not registered in Orbis under the FW or CDW NACE activities
# For FW, they are mostly related to garden waste  - garden waste falls under organic waste

# create the dataframe for all LMA entries that merged well with Orbis
LMA_Orbis_positivemerge=LMA_Orbis_merge[LMA_Orbis_merge['BvDid']!='']

# create the dataframe for all LMA entries that are from Routeverzameling
LMA_Orbis_nomerge_ROUTE=LMA_Orbis_nomerge[LMA_Orbis_nomerge['Route']=='Ja']

# create the dataframe for all LMA entries that are not linked with Orbis and are also not from Routeverzameling, these entries are exluded from the final export results
LMA_Orbis_nomerge_noroute=LMA_Orbis_nomerge[LMA_Orbis_nomerge['Route']!='Ja']

#EDIT 26 OCT
LMA_Orbis_positivemerge['Merged w Orbis']='Yes'
LMA_Orbis_nomerge_ROUTE['Merged w Orbis']='Route'
LMA_Orbis_nomerge_noroute['Merged w Orbis']='No'

#EDIT by Rusne: set all unknown NACE codes to the WU-0003 (NACE Unknown)
LMA_Orbis_nomerge_ROUTE['NACE'] = 'WU-0003'
LMA_Orbis_nomerge_noroute['NACE'] = 'WU-0003'

#######
# STEP 3 c
#######
# take out non-relevant from garden/plantsoen waste
LMA_Orbis_relevant=pd.concat([LMA_Orbis_positivemerge,LMA_Orbis_nomerge_ROUTE,LMA_Orbis_nomerge_noroute],ignore_index=True)



#######
# STEP 4
#######
# STEP 4 a
#######


# From the latest list, we take out any 'keywords' that describe waste flows only related to garden/landscape maintenance
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('sloopmaaisel', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('snoei', case=False)==True, 'Include?']= 'no'
# LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('groenafval', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('blad', case=False)==True, 'Include?']= 'no'
# LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('groen ', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('tuin', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('zand', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('grond', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('stob', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('plantsoen', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('takken', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('sloot', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('hout', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('boom', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('stam', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('stronk', case=False)==True, 'Include?']= 'no'
# LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains(' groen', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('aanvoer c.t.a.', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('grond', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('bomen', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('gras', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('snippers', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('schoffel', case=False)==True, 'Include?']= 'no'
# LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('groen', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('bos', case=False)==True, 'Include?']= 'no'
# LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('groen', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('tabak', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('schors', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('kurk', case=False)==True, 'Include?']= 'no'
# LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('greoen', case=False)==True, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('Veiling', case=False)==True, 'Include?']= 'no'


#######
# STEP 4 b
#######
# overwrite any description that nonetheless has 'GFT' included
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['BenamingAfval'].str.contains('GFT', case=False)==True, 'Include?']= 'yes'

# do not exclude anything from the CDW
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['Scope']=='CDW', 'Include?']= 'yes'


#######
# STEP 4 c
#######

# edit by Rusne
# exclude certain Eural Codes that refer to the gardening waste only
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['EuralCode']==20107, 'Include?']= 'no'
LMA_Orbis_relevant.loc[LMA_Orbis_relevant['EuralCode']==200201, 'Include?']= 'no'

#  Exclude all the LMA entries that are only referring to garden/landscaping waste
LMA_Orbis_relevant_include=LMA_Orbis_relevant[LMA_Orbis_relevant['Include?']!='no']
del LMA_Orbis_relevant_include['Include?']

#rename dataframe
LMA_w_BVDid=LMA_Orbis_relevant_include.copy()



#######
# STEP 5
#######
# provide sensitivity data only on non-route entries
LMA_sens_check=LMA_w_BVDid[LMA_w_BVDid['Route']!='Ja']
#######
# STEP 5 a
#######


#sensitivity check for NACE code - take extra attention if a NACE code has very few BVDiD entries
LMA_sens_check_nace=LMA_sens_check[['NACE','BvDid']]
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
LMA_w_BVDid=pd.merge(LMA_w_BVDid,LMA_sens_information_nace,on='NACE', how='left')
del LMA_w_BVDid['Count']
LMA_w_BVDid.loc[LMA_w_BVDid['Sensitive_NACE']!='Yes', 'Sensitive_NACE']='No'

# sensitivity on Postcode
LMA_w_BVDid=pd.merge(LMA_w_BVDid,LMA_sens_check_postcode,on='EuralCode', how='left')
del LMA_w_BVDid['Count']
LMA_w_BVDid.loc[LMA_w_BVDid['Sensitive_Postcode']!='Yes', 'Sensitive_Postcode']='No'



#######
# STEP 6
#######
# STEP 6 a
#######
#connecting 9.1 en 9.2 to Eural Codes - as preparation to use the CBS voedselverspilling data
LMA_w_BVDid=pd.merge(LMA_w_BVDid,Eural_9X,on='EuralCode',how='left')

# more preparation for linking with the CBS food waste fractions
# 'No fraction av' = no fraction available from a study


#NACE=pd.read_excel('NACE_CPA.xlsx', sheet_name='NACE-CPA 2.1')
#NACE=NACE[['CPA lv3 code','CPA lv4 code','NACE.gis']]
#NACE=NACE.drop_duplicates()


# LMA_w_BVDid['NACE']=LMA_w_BVDid['NACE'].convert_objects(convert_numeric=True)
LMA_w_BVDid.loc[LMA_w_BVDid['NACE'].str.startswith('A'), 'NACE lv2']='No fraction av (agriculture)' #in the CBS document it is stated that they were not able to make any estimation for NACE 3.XX (agriculture)


#pd.read_excel('.')

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
# else:
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1010)&(LMA_w_BVDid['NACE']<1020), 'NACE lv2']=10.1
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1020)&(LMA_w_BVDid['NACE']<1030), 'NACE lv2']=10.2
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1030)&(LMA_w_BVDid['NACE']<1040), 'NACE lv2']=10.3
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1040)&(LMA_w_BVDid['NACE']<1050), 'NACE lv2']=10.4
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1050)&(LMA_w_BVDid['NACE']<1060), 'NACE lv2']=10.5
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1060)&(LMA_w_BVDid['NACE']<1070), 'NACE lv2']=10.6
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1070)&(LMA_w_BVDid['NACE']<1080), 'NACE lv2']=10.7
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1080)&(LMA_w_BVDid['NACE']<1090), 'NACE lv2']=10.8
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1090)&(LMA_w_BVDid['NACE']<1100), 'NACE lv2']=10.9
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1100)&(LMA_w_BVDid['NACE']<1200), 'NACE lv2']=11
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1200)&(LMA_w_BVDid['NACE']<1300), 'NACE lv2']=12
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=4600)&(LMA_w_BVDid['NACE']<4700), 'NACE lv2']=46
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=4700)&(LMA_w_BVDid['NACE']<4800), 'NACE lv2']=47
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=5500)&(LMA_w_BVDid['NACE']<5600), 'NACE lv2']=55
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=5600)&(LMA_w_BVDid['NACE']<5700), 'NACE lv2']=56
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=8500)&(LMA_w_BVDid['NACE']<8600), 'NACE lv2']='P'
#     LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=8600)&(LMA_w_BVDid['NACE']<8700), 'NACE lv2']=86

"""
# for each NACE code (if relevant to the CBS study), add their NACE code aggregate for one level higher (or could actually be level 3 in reality, called 'NACE lv' here)
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1010)&(LMA_w_BVDid['NACE']<1020), 'NACE lv2']=10.1
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1020)&(LMA_w_BVDid['NACE']<1030), 'NACE lv2']=10.2
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1030)&(LMA_w_BVDid['NACE']<1040), 'NACE lv2']=10.3
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1040)&(LMA_w_BVDid['NACE']<1050), 'NACE lv2']=10.4
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1050)&(LMA_w_BVDid['NACE']<1060), 'NACE lv2']=10.5
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1060)&(LMA_w_BVDid['NACE']<1070), 'NACE lv2']=10.6
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1070)&(LMA_w_BVDid['NACE']<1080), 'NACE lv2']=10.7
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1080)&(LMA_w_BVDid['NACE']<1090), 'NACE lv2']=10.8
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1090)&(LMA_w_BVDid['NACE']<1100), 'NACE lv2']=10.9
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1100)&(LMA_w_BVDid['NACE']<1200), 'NACE lv2']=11
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=1200)&(LMA_w_BVDid['NACE']<1300), 'NACE lv2']=12
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=4600)&(LMA_w_BVDid['NACE']<4700), 'NACE lv2']=46
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=4700)&(LMA_w_BVDid['NACE']<4800), 'NACE lv2']=47
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=5500)&(LMA_w_BVDid['NACE']<5600), 'NACE lv2']=55
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=5600)&(LMA_w_BVDid['NACE']<5700), 'NACE lv2']=56
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=8500)&(LMA_w_BVDid['NACE']<8600), 'NACE lv2']='P'
LMA_w_BVDid.loc[(LMA_w_BVDid['NACE']>=8600)&(LMA_w_BVDid['NACE']<8700), 'NACE lv2']=86
"""
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

LMA_w_BVDid['Fraction']=LMA_w_BVDid['Fraction'].replace(np.NaN, '')
LMA_w_BVDid.loc[LMA_w_BVDid['Fraction']=='','Fraction']=1
LMA_w_BVDid.to_excel('Fractions.xlsx')

#######
# STEP 7
#######
#add our (english) categorization of the waste treatment process description
WT_descr=pd.read_excel('Preprocessing_description.xlsx')
WT_descr.drop_duplicates(inplace=True)
LMA_w_BVDid=pd.merge(LMA_w_BVDid,WT_descr,on='VerwerkingsOmschrijving', how='left')


#_____________________________________________________________________________
#_____________________________________________________________________________
# E X P O R T I N G     C O M P R E H E N S I V E    F I L E
#_____________________________________________________________________________
#_____________________________________________________________________________

#######
# STEP 8
#######
# STEP 8 a
#######
#%%
os.chdir(Exportfolder)
LMA_w_BVDid.to_excel('Export_LMA_Analysis_comprehensive.xlsx')
#_____________________________________________________________________________
#_____________________________________________________________________________
# C O N V E R T    T O   G D S E    C O M P L I A N T    T A B L E S
#_____________________________________________________________________________
#_____________________________________________________________________________

#######
# STEP 8 b
#######

LMA_w_BVDid_toGDSE=LMA_w_BVDid.copy()
LMA_w_BVDid_toGDSE['Source']='lma2016'
LMA_w_BVDid_toGDSE['Year']=Year

# PREPARING COMPOSITION TABLE
Composition_table_prep=LMA_w_BVDid_toGDSE.copy()
Composition_table_prep['Avoidable'] = 'FALSE' #must still check with definitions
Composition_table_prep=Composition_table_prep[['NACE',
                                               'EuralCode',
                                               'BenamingAfval',
                                               'Fraction',
                                               'Avoidable',
                                               'Source',
                                               'Year',
                                               'Scope']]

Composition_table=Composition_table_prep.drop_duplicates()
Composition_table.rename(columns={'NACE':'NACE',
                                  'EuralCode':'Custom name',
                                  'BenamingAfval':'Material'},inplace=True)

Composition_table_FW = Composition_table[Composition_table['Scope'] == 'FW']
Composition_table_CDW = Composition_table[Composition_table['Scope'] == 'CDW']
Composition_table_FW.to_excel('Composition_table_company_FW.xlsx')
Composition_table_CDW.to_excel('Composition_table_company_CDW.xlsx')


#######
# STEP 8 c
#######

# PREPARING FLOW TABLE
#Verwerker still needs to be connected to BVDiD
#%%
Flow_table_prep=LMA_w_BVDid_toGDSE.copy()




#Ontdoener  - Inzamelaar - Ontvanger - Verwerker
Flow_table_prep.replace(np.NaN, '',inplace=True)
Flow_table_prep.loc[Flow_table_prep['Inzamelaar']!='', 'Chain1']='0-1'
Flow_table_prep.loc[Flow_table_prep['Inzamelaar']=='', 'Chain1']='0-2'
Flow_table_prep.loc[(Flow_table_prep['Inzamelaar']=='')&(Flow_table_prep['Ontvanger']==''), 'Chain1']='0-3'
Flow_table_prep.loc[(Flow_table_prep['Chain1']=='0-1')&(Flow_table_prep['Ontvanger']!=''), 'Chain2']='1-2'
Flow_table_prep.loc[(Flow_table_prep['Chain1']=='0-1')&(Flow_table_prep['Ontvanger']==''), 'Chain2']='1-3'
Flow_table_prep.loc[(Flow_table_prep['Chain1']=='0-2')|(Flow_table_prep['Chain2']=='1-2')&(Flow_table_prep['Verwerker']!=''), 'Chain3']='2-3'

Flow_table_herkomst_inzamelaar=Flow_table_prep[Flow_table_prep['Chain1']=='0-1']
Flow_table_herkomst_ontvanger=Flow_table_prep[Flow_table_prep['Chain1']=='0-2']
#Flow_table_herkomst_verwerker=Flow_table_prep[Flow_table_prep['Chain1']=='0-3'] #does not exist

Flow_table_inzamelaar_ontvanger=Flow_table_prep[Flow_table_prep['Chain2']=='1-2']
Flow_table_inzamelaar_verwerker=Flow_table_prep[Flow_table_prep['Chain2']=='1-3'] #also empty

Flow_table_ontvanger_verwerker=Flow_table_prep[Flow_table_prep['Chain3']=='2-3']

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

Flow_table_herkomst_inzamelaar=Flow_table_herkomst_inzamelaar[['Scope',
                                              'Afvalstroomnummer','BenamingAfval',
                                              'Ontdoener','Postcode','Herkomst_Plaats', 'Herkomst_Straat','Huisnr',
                                              'Inzamelaar','Inzamelaar_Postcode', 'Inzamelaar_Plaats','Inzamelaar_Straat', 'Inzamelaar_Huisnr',
                                              'Route','Gewicht_KG','Aantal_vrachten', 'EuralCode', 'NACE', 'Year','Source']]
Flow_table_herkomst_inzamelaar['Process'] = ''
Flow_table_herkomst_inzamelaar['Relation']='herkomst_inzamelaar'

Flow_table_herkomst_inzamelaar.columns=['Scope','Afvalstroomnummer','BenamingAfval',
                                        'Origin_Name','Origin_Postcode','Origin_Plaats', 'Origin_Straat', 'Origin_Huisnr',
                                        'Destination_Name','Destination_Postcode','Destination_Plaats','Destination_Straat', 'Destination_Huisnummer',
                                        'Route','Gewicht_KG', 'Aantal_vrachten','EuralCode',
                                        'NACE','Year','Source','Process','Relation']


Flow_table_herkomst_ontvanger=Flow_table_herkomst_ontvanger[['Scope',
                                              'Afvalstroomnummer','BenamingAfval',
                                              'Ontdoener','Postcode','Herkomst_Plaats', 'Herkomst_Straat','Huisnr',
                                              'Ontvanger','Ontvanger_Postcode','Ontvanger_Plaats','Ontvanger_Straat','Ontvanger_Huisnummer',
                                              'Route','Gewicht_KG','Aantal_vrachten', 'EuralCode', 'NACE', 'Year','Source']]
Flow_table_herkomst_ontvanger['Process'] = ''
Flow_table_herkomst_ontvanger['Relation']='Flow_table_herkomst_ontvanger'

Flow_table_herkomst_ontvanger.columns=['Scope','Afvalstroomnummer','BenamingAfval',
                                        'Origin_Name','Origin_Postcode','Origin_Plaats', 'Origin_Straat', 'Origin_Huisnr',
                                        'Destination_Name','Destination_Postcode','Destination_Plaats','Destination_Straat', 'Destination_Huisnummer',
                                        'Route','Gewicht_KG', 'Aantal_vrachten','EuralCode',
                                        'NACE','Year','Source','Process','Relation']

Flow_table_inzamelaar_ontvanger=Flow_table_inzamelaar_ontvanger[['Scope',
                                                 'Afvalstroomnummer','BenamingAfval',
                                              'Inzamelaar','Inzamelaar_Postcode','Inzamelaar_Plaats','Inzamelaar_Straat','Inzamelaar_Huisnr',
                                              'Ontvanger','Ontvanger_Postcode','Ontvanger_Plaats','Ontvanger_Straat', 'Ontvanger_Huisnummer',
                                              'Route','Gewicht_KG','Aantal_vrachten', 'EuralCode', 'NACE', 'Year','Source']]
Flow_table_inzamelaar_ontvanger['Process'] = ''
Flow_table_inzamelaar_ontvanger['Relation']='inzamelaar_ontvanger'

Flow_table_inzamelaar_ontvanger.columns=['Scope','Afvalstroomnummer','BenamingAfval',
                                        'Origin_Name','Origin_Postcode','Origin_Plaats', 'Origin_Straat', 'Origin_Huisnr',
                                        'Destination_Name','Destination_Postcode','Destination_Plaats','Destination_Straat', 'Destination_Huisnummer',
                                        'Route','Gewicht_KG', 'Aantal_vrachten','EuralCode',
                                        'NACE','Year','Source','Process','Relation']


Flow_table_inzamelaar_verwerker=Flow_table_inzamelaar_verwerker[['Scope',
                                                 'Afvalstroomnummer','BenamingAfval',
                                              'Inzamelaar','Inzamelaar_Postcode','Inzamelaar_Plaats','Inzamelaar_Straat', 'Inzamelaar_Huisnr',
                                              'Verwerker','Verwerker_Postcode','Verwerker_Plaats','Verwerker_Straat', 'Verwerker_Huisnummer',
                                              'Route','Gewicht_KG','Aantal_vrachten', 'EuralCode', 'NACE', 'Year','Source', 'Processing description']]
Flow_table_inzamelaar_verwerker['Relation']='inzamelaar_verwerker'

Flow_table_inzamelaar_verwerker.columns=['Scope','Afvalstroomnummer','BenamingAfval',
                                        'Origin_Name','Origin_Postcode','Origin_Plaats', 'Origin_Straat', 'Origin_Huisnr',
                                        'Destination_Name','Destination_Postcode','Destination_Plaats','Destination_Straat', 'Destination_Huisnummer',
                                        'Route','Gewicht_KG', 'Aantal_vrachten','EuralCode',
                                        'NACE','Year','Source','Process','Relation']

Flow_table_ontvanger_verwerker=Flow_table_ontvanger_verwerker[['Scope',
                                                 'Afvalstroomnummer','BenamingAfval',
                                                 'Ontvanger','Ontvanger_Postcode','Ontvanger_Plaats','Ontvanger_Straat','Ontvanger_Huisnummer',
                                              'Verwerker','Verwerker_Postcode','Verwerker_Plaats','Verwerker_Straat','Verwerker_Huisnummer',
                                              'Route','Gewicht_KG','Aantal_vrachten', 'EuralCode', 'NACE', 'Year','Source', 'Processing description']]
Flow_table_ontvanger_verwerker['Relation']='ontvanger_verwerker'

Flow_table_ontvanger_verwerker.columns=['Scope','Afvalstroomnummer','BenamingAfval',
                                        'Origin_Name','Origin_Postcode','Origin_Plaats', 'Origin_Straat', 'Origin_Huisnr',
                                        'Destination_Name','Destination_Postcode','Destination_Plaats','Destination_Straat', 'Destination_Huisnummer',
                                        'Route','Gewicht_KG', 'Aantal_vrachten','EuralCode',
                                        'NACE','Year','Source','Process','Relation']

Flow_table=pd.concat([Flow_table_herkomst_inzamelaar,Flow_table_herkomst_ontvanger,Flow_table_inzamelaar_verwerker,Flow_table_inzamelaar_ontvanger,Flow_table_ontvanger_verwerker],ignore_index=True)

Flow_table_FW = Flow_table[Flow_table['Scope'] == 'FW']
Flow_table_CDW = Flow_table[Flow_table['Scope'] == 'CDW']
Flow_table_FW.to_excel('Flow_table_FW.xlsx')
Flow_table_CDW.to_excel('Flow_table_CDW.xlsx')

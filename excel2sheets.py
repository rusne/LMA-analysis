# save every sheet in an excel file as a separate file
# with the chosen seprator and file extension
# files are named after the sheets

import pandas as pd

filepath = 'SandboxCity/'
filename = "Peel-pioneer-dummy.xlsx"
separator = '\t'
extension = 'tsv'
# extension = 'xlsx'

xlsx = pd.ExcelFile(filepath + filename)
for sheet in xlsx.sheet_names:
    table = xlsx.parse(sheet)
    if extension == 'xlsx':
        table.to_excel('{0}{1}.xlsx'.format(filepath, sheet), encoding='utf-8', index=False)
    else:
        table.to_csv('{0}{1}.{2}'.format(filepath, sheet, extension), separator='\t', encoding='utf-8', index=False)

import csv
import tabula
import pandas as pd

# Read pdf into list of DataFrame
main_df = pd.DataFrame()
pdf_file = '2024 Formulary AMH VIP DE.pdf'
dfs = tabula.read_pdf(pdf_file, pages='10-11', stream=True, pandas_options={'header': None}, lattice=True)
for i in dfs:
    df = pd.DataFrame(i)

    # Headers
    df.drop(index=0)
    headers = df.iloc[0].values
    df.columns = headers
    df.drop(index=0, axis=0, inplace=True)

    df = df.replace(r'\r+|\n+|\t+','', regex=True)
    df = df.dropna(axis=1,how='all')
    main_df = pd.concat([main_df, df])

data = pd.DataFrame()
main_df.to_csv('test.csv', sep='|', index=False)
with open('test.csv', mode ='r')as file:
  csv_file = csv.reader(file, delimiter='|')
  for line in csv_file:
    line_list = list(line)
    #if line_list[1] == '1':
    #    line_list.pop(1)
    
    if line_list[0] != '':
        if line_list[1] == '':
           print(line_list)
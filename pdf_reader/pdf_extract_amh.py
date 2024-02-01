import pandas as pd
import logging
import tabula
import csv
import os

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#Hard-coded values
input_path = '.\\pdf_reader\\input_amh\\'
output_path = '.\\pdf_reader\\output_amh\\'
drug_tier_list = ['1', '2', '3', '4', '5', '1.0', '2.0', '3.0', '4.0', '5.0', ]

def get_pdf_list():
    pdf_list = []
    file_list = os.listdir(input_path)
    for file in file_list:
        if file.endswith('.pdf'):
            pdf_list.append(file)

    return pdf_list

def convert_pdf_to_csv(pdf_file):
    main_df = pd.DataFrame()
    output_name = str(pdf_file).split('.')[0] + '.tmp'
    dfs = tabula.read_pdf(input_path + pdf_file, pages='all', stream=True, pandas_options={'header': None}, lattice=True)
    for i in dfs:
        df = pd.DataFrame(i)
        df = df.replace(r'\r+|\n+|\t+','', regex=True)
        df = df.dropna(axis=1, how='all')
        main_df = pd.concat([main_df, df])

    main_df.to_csv(output_name, sep='|', index=False)
    return output_name

def process_amh_csv(tmp_file):
    data = dict()
    with open(tmp_file, mode ='r')as file:
        tmp_file = csv.reader(file, delimiter='|')
        active_status = 0
        counter = 0
        for line in tmp_file:
            if line[0] == 'Drug Name':
                active_status = 1
                
            if active_status == 1:
                if any(x.strip() for x in line):
                    old_line = counter
                    counter += 1
                    if line[0]:
                        if line[0] in drug_tier_list:
                            drug_tier = line[0]
                            for k, v in data.items():
                                if k == old_line:
                                    v = v.replace('||', '|{}|'.format(drug_tier))
                                    data[k] = v
                        else:
                            drug_name = line[0]
                            drug_tier = get_drug_tier(line)
                            drug_limit = get_drug_limit(line)
                            data[counter] = drug_name + '|' + str(drug_tier) + '|' + drug_limit
                    else:
                        drug_tier = get_drug_tier(line)
                        for k, v in data.items():
                            if k == old_line:
                                v = v.replace('||', '|{}|'.format(drug_tier))
                                data[k] = v

    return data

def get_drug_tier(line):
    drug_tier = ''
    if line[1] in drug_tier_list:
        drug_tier = int(float(line[1]))
    elif line[2] in drug_tier_list:
        drug_tier = int(float(line[2]))

    return drug_tier

def get_drug_limit(line):
    drug_limit = ''
    if line[3] not in drug_tier_list and line[3] != '':
        drug_limit = line[3]
    elif line[2] not in drug_tier_list and line[2] != '':
        drug_limit = line[2]

    return drug_limit

def get_ignore_list():
    with open('.\\pdf_reader\\ignore_list.txt') as f:
        ignore_list = f.read().splitlines()
    f.close()

    return ignore_list

def main():
    pdf_list = get_pdf_list()
    ignore_list = get_ignore_list()
    for pdf_file in pdf_list:
        file_name = convert_pdf_to_csv(pdf_file)
        data = process_amh_csv(file_name)
        output_file = file_name.split('.')[0] + '.csv'
        file = open(output_path + output_file, 'w')
        for k, v in data.items():
            data_list = str(v).split('|')
            if data_list[0] not in ignore_list:
                file.write(str(v))
                file.write('\n')

        file.close()
        os.remove(file_name)

main()
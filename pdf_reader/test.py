from pathlib import Path
import pandas as pd
import logging
import tabula
import csv
import os

# Logger
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Path
input_path = '.\\pdf_reader\\input_amh\\'
output_path = '.\\pdf_reader\\output_amh\\'
ignore_file_path = '.\\pdf_reader\\ignore_list.csv'
drug_class_file_path = '.\\pdf_reader\\amh_drug_class.csv'
Path(output_path).mkdir(parents=True, exist_ok=True)

# Hard Coded Values
drug_tier_list = ['1', '2', '3', '4', '5', '1.0', '2.0', '3.0', '4.0', '5.0', ]

def get_pdf_list(input_file_path):
    logger.info('Getting files from {}'.format(input_file_path))
    pdf_list = []
    file_list = os.listdir(input_file_path)
    for file in file_list:
        if file.endswith('.pdf'):
            pdf_list.append(file)

    return pdf_list

def get_list_from_file(input_file, sep='|'):
    with open(input_file, encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=sep)
        data_list = list(csv_reader)
    f.close()

    return data_list

def get_drug_dict(drug_list):
    drug_def = [row[0] for row in drug_list]
    drug_type = [row[1] for row in drug_list]
    drug_code = [row[2] for row in drug_list]

    drug_dict = {drug_code[i]: drug_def[i] + '|' + drug_type[i] for i in range(len(drug_code))}

    return drug_dict, drug_code

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

def convert_pdf_to_csv(file_path='.\\', pdf_file='test.pdf'):
    logger.info('....Converting {} to CSV.'.format(pdf_file))
    main_df = pd.DataFrame()
    output_name = str(pdf_file).split('.')[0] + '.tmp'
    dfs = tabula.read_pdf(
                            file_path + pdf_file, 
                            pages='all', 
                            stream=True, 
                            pandas_options={'header': None}, 
                            lattice=True
                        )
    for i in dfs:
        df = pd.DataFrame(i)
        df = df.replace(r'\r+|\n+|\t+','', regex=True)
        df = df.dropna(axis=1, how='all')
        main_df = pd.concat([main_df, df])

    main_df.to_csv(output_name, sep='|', index=False)
    logger.info('........{} created for processing.'.format(output_name))

    return output_name

def process_amh_csv(tmp_file):
    logger.info('............Processing {}'.format(tmp_file))
    
    data = dict()
    drug_data = dict()
    drug_data[0] = None
    counter = 0
    active_status = 0
    active_val = 0

    drug_list = get_list_from_file('.\\pdf_reader\\amh_drug_class.csv')
    drug_dict, drug_code = get_drug_dict(drug_list)
    lines = get_list_from_file(tmp_file)

    for line in lines:
        drug_name = line[0]
        old_line = counter
        counter += 1

        if drug_name == 'Drug Name':
            active_status = 1

        if active_status == 1:
            if any(x.strip() for x in line):
                if drug_name and drug_name not in ('Drug Name'):
                    if drug_name in drug_tier_list:
                        drug_tier = drug_name
                        for k, v in data.items():
                            if k == old_line:
                                v = v.replace('||', '|{}|'.format(drug_tier))
                                data[k] = v
                    else:
                        drug_tier = get_drug_tier(line)
                        drug_limit = get_drug_limit(line)
                        data[counter] = drug_name + '|' + str(drug_tier) + '|' + drug_limit

                    if drug_name.strip() in drug_code:  
                        drug_data[counter] = drug_dict[drug_name]
                        active_val = counter
                    else:
                        drug_data[counter] = drug_data[active_val]
                else:
                    drug_tier = get_drug_tier(line)
                    for k, v in data.items():
                        if k == old_line:
                            v = v.replace('||', '|{}|'.format(drug_tier))
                            data[k] = v

    return data, drug_data

def main():    
    pdf_list = get_pdf_list(input_path)
    ignore_file = get_list_from_file('.\\pdf_reader\\ignore_list.csv')
    ignore_list = []

    for i in ignore_file:
        ignore_list.append(i[0])

    for pdf_file in pdf_list:
        logger.info('Loading {}'.format(pdf_file))
        file_name = convert_pdf_to_csv(input_path, pdf_file)        
        data, drug_data = process_amh_csv(file_name)
        output_file = file_name.split('.')[0] + '.csv'
        file = open(output_path + output_file, 'w')
        for k, v in data.items():
            data_list = str(v).split('|')
            if data_list[0] not in ignore_list:
                file.write(drug_data[k] + '|' + str(v))
                file.write('\n')

        file.close()
        os.remove(file_name)
        logger.info('................Done processing {}'.format(pdf_file))
        logger.info('....................Output: {}'.format(output_path + output_file))

if __name__ == "__main__":
    main()
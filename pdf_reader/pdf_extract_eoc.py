import pandas as pd
import logging
import tabula
import fitz
import csv
import os
from pathlib import Path

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#Hard-coded values
input_path = '.\\pdf_reader\\input_eoc\\'
output_path = '.\\pdf_reader\\output_eoc\\'

Path(input_path).mkdir(parents=True, exist_ok=True)

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
    dfs = tabula.read_pdf(input_path + pdf_file, pages='all')
    for i in dfs:
        df = pd.DataFrame(i)
        main_df = pd.concat([main_df, df])

    main_df.to_csv(output_name, sep='|', index=False)
    return output_name

pdf_list = get_pdf_list()
for pdf_file in pdf_list:
    csv_file = convert_pdf_to_csv(pdf_file)
    with open(csv_file, 'r', encoding='utf-8') as file:
        tmp_file = csv.reader(file, delimiter='|')
        line_number = 0
        start_line = 0
        start_string = 'Services that are covered for you'
        for line in tmp_file:
            line_number += 1
            if start_string in line:
                start_line = line_number
                break            


        for line in tmp_file:
            if line_number == 146:
                print(line)
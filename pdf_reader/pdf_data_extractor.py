import pandas as pd
import fitz
import os

#Hard-coded values
input_path = '.\\pdf_reader\\input\\'
output_path = '.\\pdf_reader\\output\\'
df = pd.DataFrame(columns=['drug_type', 'drug_name', 'drug_tier', 'requirements_limits'])


def read_pdf(pdf_file):
    full_pdf_path = input_path + pdf_file
    doc = fitz.open(full_pdf_path)

    return doc


def extract_data_from_pdf(doc, start_page, end_page=999):
    drug_type = ''
    for page in doc:
        page_list = str(page).split(' ')
        page_number = int(page_list[1])
        if page_number >= start_page and page_number <= end_page:
            tabs = page.find_tables()
            tab = tabs[0]
            for line in tab.extract():
                if 'Drug Tier' not in line: #Value: None, 'Drug Tier', None
                    if None in line:                    
                        drug_type = line[0]

                    line.insert(0, drug_type)
                    df.loc[len(df)] = line


list_pdf = os.listdir(input_path)
for file in list_pdf:
    if file.endswith('.pdf'):
        pdf_input = str(file)

        doc = read_pdf(pdf_input)
        extract_data_from_pdf(doc, 10, 99)
        df = df.dropna()
        df.to_excel(output_path + '{output_name}.xlsx'.format(output_name=pdf_input), index=False)
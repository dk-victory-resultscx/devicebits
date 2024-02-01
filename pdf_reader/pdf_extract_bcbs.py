import logging
import pandas as pd
import fitz #PyMuPDF
import os

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#Hard-coded values
input_path = '.\\pdf_reader\\input_bcbs\\'
output_path = '.\\pdf_reader\\output_bcbs\\'


def get_pdf_list():
    pdf_list = []
    file_list = os.listdir(input_path)
    for file in file_list:
        if file.endswith('.pdf'):
            pdf_list.append(file)

    return pdf_list


def read_pdf(pdf_file):
    full_pdf_path = input_path + pdf_file
    doc = fitz.open(full_pdf_path)

    return doc


def get_page_number(pdf_file):
    start_page = 1
    end_page = 999
    doc = read_pdf(pdf_file)
    for page in doc:
        page_list = str(page).split(' ')
        page_number = int(page_list[1])
        page_keyword_1 = page.search_for('Drug Name')
        page_keyword_2 = page.search_for('Drug Tier')
        page_keyword_3 = page.search_for('Requirements/Limits')

        if page_keyword_1 and page_keyword_2 and page_keyword_3 and page_number > 7:
            start_page = page_number
            break

    for page in doc:
        page_list = str(page).split(' ')
        page_number = int(page_list[1])
        page_keyword_1 = page.search_for('Drug Name')
        page_keyword_2 = page.search_for('Drug Tier')
        page_keyword_3 = page.search_for('Requirements/Limits')
        
        if page_keyword_1 and page_keyword_2 and page_keyword_3 and page_number > 7:
            end_page = page_number

    return start_page, end_page


def process_single_formulary(pdf_file, start_page, end_page):
    drug_type = ''
    output_name = str(pdf_file).split('.')[0]
    formulary_df = pd.DataFrame(columns=['drug_type', 'drug_name', 'drug_tier', 'requirements_limits'])
    doc = read_pdf(pdf_file)
    for page in doc:
        page_list = str(page).split(' ')
        page_number = int(page_list[1])
        if page_number >= start_page and page_number <= end_page:
            tabs = page.find_tables()
            tab = tabs[0]
            for line in tab.extract():
                if 'Drug Tier' not in line:
                    if None in line:
                        drug_type = line[0]

                    line.insert(0, drug_type)
                    formulary_df.loc[len(formulary_df)] = line

    formulary_df = formulary_df.dropna()
    formulary_df.to_excel(output_path + '{}.xlsx'.format(output_name), index=False)


def main():
    pdf_list = get_pdf_list()
    for pdf_file in pdf_list:
        logging.info('Processing {}'.format(pdf_file))
        start_page, end_page = get_page_number(pdf_file)
        process_single_formulary(pdf_file, start_page, end_page)


main()

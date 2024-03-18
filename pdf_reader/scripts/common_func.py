import pandas as pd
import tabula
import fitz
import os, re
import pdfplumber

# Variables

def get_pdf_list(input_path):
    pdf_list = []
    file_list = os.listdir(input_path)
    for file in file_list:
        if file.endswith('.pdf'):
            pdf_list.append(file)

    return pdf_list

def csv_to_list(csv_file):
    with open(csv_file) as f:
        ignore_list = f.read().splitlines()
    f.close()

    return ignore_list

def read_pdf_fitz(input_path, pdf_file):
    full_pdf_path = input_path + pdf_file
    doc = fitz.open(full_pdf_path)

    return doc

def read_pdf_tabula(input_path, pdf_file):
    main_df = pd.DataFrame()
    dfs = tabula.read_pdf(input_path + pdf_file, pages='all', stream=True, pandas_options={'header': None}, lattice=True)
    for i in dfs:
        df = pd.DataFrame(i)
        df = df.replace(r'\r+|\n+|\t+','', regex=True)
        df = df.dropna(axis=1, how='all')
        main_df = pd.concat([main_df, df])

    return main_df

def get_page_to_process_fitz(doc):
    pages = list()
    for page in doc:
        page_list = str(page).split(' ')
        page_number = int(page_list[1])
        page_keyword_1 = page.search_for('Drug Name')
        page_keyword_2 = page.search_for('Drug Tier')
        page_keyword_3 = page.search_for('Requirements/Limits')        

        if page_keyword_1 and page_keyword_2 and page_keyword_3 and page_number > 7:
            pages.append(page_number)

    return min(pages), max(pages)

def get_drug_tier(line, drug_tier_list):
    drug_tier = ''
    if line[1] in drug_tier_list:
        drug_tier = int(float(line[1]))
    elif line[2] in drug_tier_list:
        drug_tier = int(float(line[2]))

    return drug_tier

def get_drug_limit(line, drug_tier_list):
    drug_limit = ''
    if line[3] not in drug_tier_list and line[3] != '':
        drug_limit = line[3]
    elif line[2] not in drug_tier_list and line[2] != '':
        drug_limit = line[2]

    return drug_limit

def generate_eoc_image(image_path, input_path, pdf_file, config):
    pdf = pdfplumber.open(input_path + pdf_file)
    png_file = str(pdf_file).split('.')[-2] + '.png'
    for page in pdf.pages:
        page_name = str(page).replace('<', '').replace('>', '').replace(':', '_') + '.png'
        table = page.extract_table()
        if table != None:
            if 'Services that are covered' in str(table):
                im = page.to_image()
                im.debug_tablefinder({
                    "explicit_vertical_lines": config,
                })
                im.save(image_path + page_name)

def set_margin(pdf_file):
    name_list = str(pdf_file).split('-')
    name_var = name_list[0] + name_list[2]
    
    switch={
        'mappo': [70, 370, 540],
        'mapdhmo': [70, 370, 540],
        'mapdhmopos': [70, 370, 540],
        'mapdppo': [70, 345, 540]
    }

    return switch.get(name_var, 'Invalid file name.')

def purge(dir, pdf_file):
    pdf_file_name = str(pdf_file).split('.')[0]
    for f in os.listdir(dir):
        if re.search('{}.*\.csv$'.format(pdf_file_name), f):
            os.remove(os.path.join(dir, f))

def draw_line(file_name):
    file_name.write(('\n' + ('-'  * 87) + '\n').encode('utf-8'))

def get_chapter(text):
    if re.match('^CHAPTER\s+\d+:$', text.rstrip()):
        text_list = text.rstrip().split(' ')
        chapter = text_list[0] + ' ' + text_list[-1].replace(':', '')
        
        return chapter
    
def get_section(text, pattern):
    if re.match(pattern, text):
        line_list = text.split(' ')
        section = line_list[0] + ' ' + line_list[1]

        return section
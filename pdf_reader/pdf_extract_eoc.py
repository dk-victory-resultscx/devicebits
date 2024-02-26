import pandas as pd
import pdfplumber
import logging
import csv
import os

# Logger
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Hard-coded values
input_path = '.\\pdf_reader\\input_eoc\\'
output_path = '.\\pdf_reader\\output_eoc\\'
image_path = '.\\pdf_reader\\img_eoc\\'

def get_pdf_list():
    logger.info('Getting files from {}'.format(input_path))
    pdf_list = []
    file_list = os.listdir(input_path)
    for file in file_list:
        if file.endswith('.pdf'):
            pdf_list.append(file)

    return pdf_list


def get_service_list():
    with open('.\\pdf_reader\\service_list.csv') as f:
        service_list = f.read().splitlines()
    f.close()

    return service_list


def generate_eoc_csv(pdf_file):
    ma_ppo = [70, 370, 540]
    mapd_hmo = [70, 370, 540]
    mapd_eoc = [70, 345, 540]
    pdf = pdfplumber.open(input_path + pdf_file)
    logger.info('....Converting {} to CSV.'.format(pdf_file))    
    csv_file = pdf_file.split('.')[-2] + '.csv'
    with open(csv_file, 'w', encoding='utf-8') as file:
        for page in pdf.pages:
            table = page.extract_table(table_settings={"explicit_vertical_lines": mapd_eoc })
            if table != None:
                if 'Services that are covered' in str(table):                
                    for i in table:
                        if i[0] not in ('Services that are covered', 'Medical Benefits Chart'):
                            if str(i[1]) not in ('Services that are covered'):
                                if i[0] not in ('', 'None', None) and i[2] not in ('', 'None', None):
                                    for element in i:
                                        if element == '':
                                            element = 'None'
                                        file.write(str(element).replace('\n', ' ') + '|')
                                    file.write('\n')
    file.close()
    logger.info('........{} created for processing.'.format(csv_file))
    return csv_file


def process_eoc_csv(csv_file):
    logger.info('............Processing {}'.format(csv_file))
    service_list = get_service_list()
    xlsx_file = str(csv_file).split('.')[-2] + '.xlsx'
    service_dict = dict()
    requirement_dict = dict()
    df = pd.DataFrame(columns=['Services that are covered for you', 'What you must pay when you get these services'])
    with open(csv_file, 'r', encoding='utf-8') as file:
        tmp_file = csv.reader(file, delimiter='|')    
        counter = 0
        for line in tmp_file:
            services = line[0]
            requirements = line[2]

            if any(map(services.startswith, service_list)):
                service_dict[counter] = services
                requirement_dict[counter] = requirements
            else:
                counter -= 1
                service_dict[counter] = service_dict[counter] + ' ' + services
                requirement_dict[counter] = requirement_dict[counter] + ' ' + requirements

            counter += 1

    for k, v in service_dict.items():
        df.loc[k, 'Services that are covered for you'] = v

    for k, v in requirement_dict.items():
        df.loc[k, 'What you must pay when you get these services'] = v

    logger.info('................Done processing {}'.format(csv_file))
    logger.info('....................Output: {}'.format(output_path + xlsx_file))

    df.to_excel(output_path + xlsx_file, index=False)
    os.remove(csv_file)

def generate_eoc_image(pdf_file):
    pdf = pdfplumber.open(pdf_file)
    png_file = str(pdf_file).split('.')[-2] + '.png'
    for page in pdf.pages:
        table = page.extract_table()
        if table != None:
            if 'Services that are covered' in str(table):
                im = page.to_image()
                im.debug_tablefinder({
                    "explicit_vertical_lines": [ 70, 370, 540 ],
                })
                im.save(image_path + png_file)

def main():
    pdf_list = get_pdf_list()    
    for pdf_file in pdf_list:
        logger.info('Loading {}'.format(pdf_file))
        #generate_eoc_image(pdf_file)
        csv_file = generate_eoc_csv(pdf_file)
        process_eoc_csv(csv_file)

if __name__ == '__main__':
    main()
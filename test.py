import pdfplumber
import string
import re

pattern = r'^[' + string.punctuation + ']+'

pdf_file = 'sample.pdf'

pdf_file_name = str(pdf_file).split('.')[0]
pdf = pdfplumber.open(pdf_file)
section = 'INITIAL'
output = open('sum_output.csv', 'wb')
title_list = ['MONTHLY PREMIUM, DEDUCTIBLE, AND LIMITS ON HOW MUCH YOU PAY FOR COVERED', 'SERVICES', 'COVERED MEDICAL AND HOSPITAL BENEFITS']

for page in pdf.pages:
    bounding_box = (0, 0, 550, 720)
    crop_area = page.within_bbox(bounding_box)
    content = crop_area.extract_text(
                                x_tolerance=1
                                ,y_tolerance=3
                                ,layout=False
                                )

    lines = content.splitlines()
    for line in lines:
        if any(map(line.startswith, ('SECTION', 'DISCLAIMERS'))):
            section = line

    if section == 'SECTION II - SUMMARY OF BENEFITS':
        table = page.extract_table()
        if table:
            for data in table:
                data = list(map(lambda x: str(x).replace('\n', ' '), data))
                new_line = '\n'.encode('utf-8')
                data_b = list(map(lambda x: x.encode('utf-8'), data))

                if data[1] in title_list:
                    output.write(new_line)
                    output.write(data_b[1])
                else:
                    if len(data) == 4:
                        if data[1] not in ('Additional', 'Member', 'Benefits'):
                            if data[2] not in ('None', '', None):
                                output.write(new_line)
                                output.write(data_b[0] + '|'.encode('utf-8') +  data_b[2])
                            else:
                                if re.search(pattern, data[0]) is not None or data[0] in ('None', '', None):
                                    output.write(data_b[3])
                                else:
                                    output.write(new_line)
                                    output.write(data_b[0] + '|'.encode('utf-8') +  data_b[3])
                    elif len(data) == 2:
                        if data[0]:
                            output.write(new_line)
                            output.write(data_b[0] + '|'.encode('utf-8') +  data_b[1])
                        else:
                            output.write(data_b[1] + ' '.encode('utf-8'))
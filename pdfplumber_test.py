from pdf_reader.scripts import common_func
import pdfplumber
import os, re

# Hard-coded values
input_path = '.\\pdf_reader\\input\\amh\\'
output_path = '.\\pdf_reader\\output\\amh\\'
pdf_file = 'sample.pdf'

def initial_pages(page, file_name, pdf_file_name):
    bounding_box = (80, 100, 550, 800)            
    crop_area = page.within_bbox(bounding_box)

    file_content = open('{} {}.csv'.format(pdf_file_name, file_name), 'ab')
    content = crop_area.extract_text(
                                    x_tolerance=1
                                    ,y_tolerance=3
                                    ,layout=False
                                    ).strip().encode('utf-8')
    file_content.write(content + '\n'.encode('utf-8'))
    file_content.close()

def extact_text(pdf_file):
    pdf_file_name = str(pdf_file).split('.')[0]
    pdf = pdfplumber.open(pdf_file)
    chapter = str()
    section = str()
    sub_section = str()
    new_line = '\n'.encode('utf-8')

    for page in pdf.pages:
        bounding_box = (80, 100, 550, 800)            
        crop_area = page.within_bbox(bounding_box)        

        if page.page_number == 1:
            initial_pages(page, 'INTRO', pdf_file_name)
        elif page.page_number > 1 and page.page_number < 5:
            initial_pages(page, 'TOC', pdf_file_name)
        else:
            content = crop_area.extract_text(
                                            x_tolerance=1
                                            ,y_tolerance=1
                                            ,layout=False
                                            ).encode('utf-8')

            lines = content.splitlines()
            for line in lines:
                decoded_line = line.decode('utf-8')
                line_chapter = common_func.get_chapter(decoded_line)
                chapter = line_chapter if line_chapter else chapter
                file_chapter = open('{} {}.csv'.format(pdf_file_name, chapter), 'ab')

                if re.match('^SECTION \d+', decoded_line):
                    section = common_func.get_section(decoded_line, '^SECTION \d+')
                    common_func.draw_line(file_chapter)
                    file_chapter.write(line + new_line)
                else:
                    if re.match('^Section \d+', decoded_line):
                        line_section = common_func.get_section(decoded_line, '^Section \d+')
                        sub_section = line_section if line_section else sub_section

                        if decoded_line.startswith(section.capitalize()):
                            file_chapter.write('\n*'.encode('utf-8') + line + new_line)
                        else:
                            file_chapter.write(line + new_line)
                    else:
                        file_chapter.write(line + new_line)

        if chapter == 'CHAPTER 4' and sub_section in ('Section 5.2', 'Section 5.3', 'Section 5.4', 'Section 5.5'):
            fix_table(page, sub_section, file_chapter)

def fix_table(page, section, csv_file):
    margin = {
                'Section 5.2': [80, 165, 235, 305, 375, 450, 550]
                ,'Section 5.3': [80, 165, 235, 305, 375, 450, 550]
                ,'Section 5.4': [80, 200, 320, 440, 550]
                ,'Section 5.5': [80, 200, 320, 440, 550]
            }

    table = page.extract_table(
        table_settings={
            'explicit_vertical_lines': margin[section]
        }
    )

    if table:
        if any('Tier' in x for x in table):
            csv_file.write(('--------------------VISUAL TABLE--------------------\n').encode('utf-8'))
            for data_list in table:
                data_list = list(map(lambda x: str(x).replace('\n', ' '), data_list))
                if data_list[0] and 'Tier' in data_list[0]:
                    for i in data_list:
                        csv_file.write((i + '|').encode('utf-8'))
                    csv_file.write('\n'.encode('utf-8'))
            csv_file.write(('----------------------------------------------------\n\n').encode('utf-8'))

common_func.purge(os.curdir, 'sample.pdf')
extact_text('sample.pdf')

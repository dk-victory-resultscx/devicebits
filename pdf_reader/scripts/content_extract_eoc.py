import common_func
import pdfplumber
import re, os

# Hard-coded values
input_path = os.getcwd() + '\\pdf_reader\\input\\pdp\\'
output_path = os.getcwd() + '\\pdf_reader\\output\\pdp\\'
pdf_file = 'sample.pdf'

def initial_pages(page, file_name, pdf_file_name):
    bounding_box = (80, 100, 550, 800)            
    crop_area = page.within_bbox(bounding_box)

    file_content = open(output_path + '{} {}.csv'.format(pdf_file_name, file_name), 'ab')
    content = crop_area.extract_text(
                                    x_tolerance=1
                                    ,y_tolerance=3
                                    ,layout=False
                                    ).strip().encode('utf-8')
    file_content.write(content + '\n'.encode('utf-8'))
    file_content.close()

def extract_text(pdf_file):
    pdf_file_name = str(pdf_file).split('.')[0]
    pdf = pdfplumber.open(input_path + pdf_file)
    chapter, section, sub_section = str(), str(), str()
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
                file_chapter = open(output_path + '{} {}.csv'.format(pdf_file_name, chapter), 'ab')

                if re.match('^SECTION \d+', decoded_line):
                    section = common_func.get_section(decoded_line, '^SECTION \d+')
                    common_func.draw_line(file_chapter)
                    file_chapter.write(line + new_line)
                elif re.match('^Section \d+', decoded_line):
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

def main():
    pdf_list = common_func.get_pdf_list(input_path)
    for pdf_file in pdf_list:
        common_func.purge(output_path, pdf_file)
        extract_text(pdf_file)

if __name__ == '__main__':
    main()

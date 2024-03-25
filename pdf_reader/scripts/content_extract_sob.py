import pdfplumber
import common_func

# Hard-coded values
input_path = '.\\pdf_reader\\input\\sob\\'
output_path = '.\\pdf_reader\\output\\sob\\'

def open_pdf(pdf_file):
    pdf = pdfplumber.open(pdf_file)

    return pdf

def get_data(page):
    bounding_box = (0, 0, 550, 720)
    crop_area = page.within_bbox(bounding_box)
    content = crop_area.extract_text(
                                x_tolerance=1
                                ,y_tolerance=3
                                ,layout=False
                                )

    lines = content.splitlines()
    table = page.extract_table()
    return lines, content.encode('utf-8'), table

def write_table(output, col1, col2):
    new_line = '\n'.encode('utf-8')
    output.write(new_line)
    output.write(col1 + '|'.encode('utf-8') +  col2)

def len4_data(data, data_b, output):
    if data[1] not in ('Additional', 'Member', 'Benefits'):
        if data[2] not in ('None', '', None):
            write_table(output, data_b[0], data_b[2])
        else:
            if data[0] in ('None', '', None):
                output.write(data_b[3])
            else:
                write_table(output, data_b[0], data_b[3])

def len2_data(data, data_b, output):
    if data[0]:
        write_table(output, data_b[0], data_b[1])
    else:
        output.write(data_b[1] + ' '.encode('utf-8'))

def prep_data(data):
    data = list(map(lambda x: str(x).replace('\n', ' '), data))
    data_b = list(map(lambda x: x.encode('utf-8'), data))

    return data, data_b

def main():
    pdf_list = common_func.get_pdf_list(input_path)

    for pdf_file in pdf_list:
        common_func.purge(output_path, pdf_file)
        section = 'INTRODUCTION'
        pdf = open_pdf(input_path + pdf_file)
        title_list = ['MONTHLY PREMIUM, DEDUCTIBLE, AND LIMITS ON HOW MUCH YOU PAY FOR COVERED', 'SERVICES', 'COVERED MEDICAL AND HOSPITAL BENEFITS']

        for page in pdf.pages:
            lines, content, table = get_data(page)

            for line in lines:
                if any(map(line.startswith, ('SECTION', 'DISCLAIMERS'))):
                    section = line

            output = open(output_path + str(pdf_file).split('.')[0]  + ' ' + section + '.csv', 'ab')
            if section != 'SECTION II - SUMMARY OF BENEFITS':
                output.write(content + '\n'.encode('utf-8'))
            else:
                if table and len(table) > 2:
                    for data in table:
                        data, data_b = prep_data(data)

                        if data[1] in title_list:
                            output.write('\n'.encode('utf-8') + data_b[1])
                        else:
                            if len(data) == 4:
                                len4_data(data, data_b, output)
                            elif len(data) == 2:
                                len2_data(data, data_b, output)

if __name__ == '__main__':
    main()
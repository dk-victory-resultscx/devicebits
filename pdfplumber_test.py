import pdfplumber

def generate_csv():
    pdf = pdfplumber.open("test.pdf")
    with open('test2.csv', 'w', encoding='utf-8') as file:
        for page in pdf.pages:
            table = page.extract_table(table_settings={"explicit_vertical_lines": [70, 370, 540]})
            if table != None:
                if 'Services that are covered for you' in str(table):                
                    for i in table:
                        if i[0] not in ('Services that are covered for you', 'Medical Benefits Chart'):
                            if str(i[1]) not in ('Services that are covered for you'):
                                if i[0] != '' or i[2] != '':
                                    for element in i:
                                        if element == '':
                                            element = 'None'
                                        file.write(str(element).replace('\n', ' ') + '|')
                                    file.write('\n')
    file.close()


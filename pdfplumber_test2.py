import pdfplumber


pdf = pdfplumber.open("test.pdf")
with open('pdfplumber_tables.csv', 'w') as file:
    for page in pdf.pages:
        table = page.extract_table()
        #table = page.extract_words()
        if table != None:
            if '24/7 Nurse Line Support' in str(table):
                im = page.to_image()

                im.debug_tablefinder({
                    "explicit_vertical_lines": [ 70, 370, 540 ],
                })

                im.save('test.png')
file.close()
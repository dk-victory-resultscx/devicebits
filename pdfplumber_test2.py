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

###############
list1 = [
    "foo", 
    "bar",
    "\n",
    "baz",
    "qux"
]

import itertools
result = []
for k,v in itertools.groupby(list1, key=lambda line: line==None):
    if not k:
        result.append(list(v))

print(result)
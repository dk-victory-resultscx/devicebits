# Required Libraries
import pdfplumber
import pandas as pd 



pdf = pdfplumber.open("test.pdf")
with open('pdfplumber_tables.csv', 'w') as file:
    for page in pdf.pages:
        table_setting = {
            "vertical_strategy": "lines", 
            "horizontal_strategy": "lines",
            "explicit_vertical_lines": [70, 370, 540],
            "explicit_horizontal_lines": [],
            "snap_tolerance": 3,
            "snap_x_tolerance": 3,
            "snap_y_tolerance": 3,
            "join_tolerance": 3,
            "join_x_tolerance": 3,
            "join_y_tolerance": 3,
            "edge_min_length": 3,
            "min_words_vertical": 3,
            "min_words_horizontal": 3,
            "text_tolerance": 3,
            "text_x_tolerance": 3,
            "text_y_tolerance": 3,
            "intersection_tolerance": 3,
            "intersection_x_tolerance": 30,
            "intersection_y_tolerance": 3,
        }
        table = page.extract_table(table_settings=table_setting)
        #table = page.extract_words()
        if table != None:
            if '24/7 Nurse Line Support' in str(table):
                #print(page.lines)
                #print(page.rects)
                #print(page.find_tables())
                for i in table:
                    file.write(str(i))
                    file.write('\n')
                break
file.close()
# Required Libraries
import pdfplumber
import pandas as pd 

table_setting = {
    "vertical_strategy": "lines", 
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [10],
    "explicit_horizontal_lines": [],
    "snap_tolerance": 3,
    "snap_x_tolerance": 3,
    "snap_y_tolerance": 3,
    "join_tolerance": 3,
    "join_x_tolerance": 3,
    "join_y_tolerance": 3,
    "edge_min_length": 3,
    "min_words_vertical": 3,
    "min_words_horizontal": 1,
    "text_tolerance": 3,
    "text_x_tolerance": 3,
    "text_y_tolerance": 3,
    "intersection_tolerance": 3,
    "intersection_x_tolerance": 3,
    "intersection_y_tolerance": 3,
}

pdf = pdfplumber.open("ma-eoc-ppo-protect-il-2024.pdf")
with open('pdfplumber2.csv', 'w') as file:
    for page in pdf.pages:
        table = page.extract_table(table_settings=table_setting)
        if table != None:
            if 'Services that are covered for you' in str(table):
                file.write(str(table))
                file.write('\n')
file.close()
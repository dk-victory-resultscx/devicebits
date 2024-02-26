import csv

def get_list_from_file(input_file, sep='|'):
    with open(input_file, encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=sep)
        data_list = list(csv_reader)
    f.close()

    return data_list

ignore_list = get_list_from_file('.\\pdf_reader\\ignore_list.csv')
a = []
for i in ignore_list:
    a.append(i[0])

print(a)
import tabula
import csv

tabula.convert_into("test.pdf", "tabula_multiple_tables.csv", output_format="csv", pages='47', multiple_tables=True)

'''
box_num = 0
data = dict()
with open('test.csv', 'r') as file:
    lines = file.readlines()
    for line in csv.reader(lines, quotechar='"', delimiter=','):
        box_num += 1
        services = line[0]
        payment = line[1]
        key_services = str(box_num) + '|services'
        key_payment = str(box_num) + '|payment'
        #print(box_num, line)
        if services and payment:
            for k, v in data.items():
                if 
            if not data[key_services]:
                data[key_services] = services
                
            
                data[str(box_num) + '|services'] = data[str(box_num) + '|services'] + services
            else:
                data[str(box_num) + '|services'] = services
            
            if data[str(box_num) + '|payment']:
                data[str(box_num) + '|payment'] = data[str(box_num) + '|payment'] + services
            else:
                data[str(box_num) + '|payment'] = payment
            
for k, v in data.items():
    print(k, '|', v)
            '''
import common_func

# Hard-coded values
input_path = '.\\pdf_reader\\input\\amh\\'
output_path = '.\\pdf_reader\\output\\amh\\'
drug_tier_list = ['1', '2', '3', '4', '5', '1.0', '2.0', '3.0', '4.0', '5.0', ]

def process_amh_df(df):
    data = dict()
    counter = 0
    flag = 0
    df = df.fillna('')
    for index, row in df.iterrows():
        line = [row[0], row[1], row[2], row[3]]
        old_line = counter
        counter += 1

        if line[0] == 'Drug Name':
            flag = 1

        if flag == 1:
            if line[0] != '':
                if line[0] in drug_tier_list:
                    drug_tier = line[0]
                    for k, v in data.items():
                        if k == old_line:
                            v = v.replace('||', '|{}|'.format(drug_tier))
                            data[k] = v
                else:
                    drug_name = line[0]
                    drug_tier = common_func.get_drug_tier(line, drug_tier_list)
                    drug_limit = common_func.get_drug_limit(line, drug_tier_list)
                    data[counter] = str(drug_name) + '|' + str(drug_tier) + '|' + str(drug_limit)
            else:
                drug_tier = common_func.get_drug_tier(line, drug_tier_list)
                for k, v in data.items():
                    if k == old_line:
                        v = v.replace('||', '|{}|'.format(drug_tier))
                        data[k] = v

    return data

def main():
    pdf_list = common_func.get_pdf_list(input_path)
    ignore_list = common_func.csv_to_list('.\\pdf_reader\\files\\amh_ignore_list.csv')

    for pdf_file in pdf_list:
        output_file = pdf_file.split('.')[0] + '.csv'

        pdf_df = common_func.read_pdf_tabula(input_path, pdf_file)
        data = process_amh_df(pdf_df)

        file = open(output_path + output_file, 'w')
        for k, v in data.items():
            data_list = str(v).split('|')
            if data_list[0] not in ignore_list:
                file.write(str(v))
                file.write('\n')
        file.close()

if __name__ == "__main__":
    main()
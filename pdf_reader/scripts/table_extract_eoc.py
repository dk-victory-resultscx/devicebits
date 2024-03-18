import common_func
import pandas as pd
import pdfplumber

# Hard-coded values
input_path = '.\\pdf_reader\\input\\eoc\\'
output_path = '.\\pdf_reader\\output\\eoc\\'
image_path = '.\\pdf_reader\\img\\eoc\\'

def generate_eoc_csv(input_path, pdf_file):
    counter = 0
    dict_service, dict_payment = dict(), dict()

    pdf = pdfplumber.open(input_path + pdf_file)
    margin = common_func.set_margin(pdf_file)
    ignore_list = common_func.csv_to_list('.\\pdf_reader\\files\\eoc_ignore_list.csv')
    service_list = common_func.csv_to_list('.\\pdf_reader\\files\\eoc_service_list.csv')    

    for page in pdf.pages:
        table = page.extract_table(table_settings={"explicit_vertical_lines": margin })

        if table != None:
            if 'Services that are covered' in str(table):
                for data_list in table:
                    data_list = list(map(lambda x: str(x).replace('\n', ' '), data_list))
                    data_list = list(map(lambda x: str(x).replace('None', ''), data_list))

                    if any(x in data_list for x in ignore_list):
                        pass
                    else:
                        if data_list[0] or data_list[2]:
                            if any(map(data_list[0].startswith, service_list)):
                                counter += 1
                                dict_service[counter] = data_list[0]
                                dict_payment[counter] = data_list[2]
                            else:
                                dict_service[counter] = dict_service[counter] + ' ' + data_list[0]
                                dict_payment[counter] = dict_payment[counter] + ' ' + data_list[2]

    return dict_service, dict_payment

def main():
    df = pd.DataFrame()
    pdf_list = common_func.get_pdf_list(input_path)

    for pdf_file in pdf_list:
        output_file = str(pdf_file).split('.')[0] + '.xlsx'
        dict_service, dict_payment = generate_eoc_csv(input_path, pdf_file)

        for k, v in dict_service.items():
            df.loc[k, 'Services that are covered for you'] = v

        for k, v in dict_payment.items():
            df.loc[k, 'What you must pay when you get these services'] = v

        df.to_excel(output_path + output_file, index=False)

if __name__ == '__main__':
    main()
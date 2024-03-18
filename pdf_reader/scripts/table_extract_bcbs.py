import pandas as pd
import common_func

#Hard-coded values
input_path = '.\\pdf_reader\\input\\bcbs\\'
output_path = '.\\pdf_reader\\output\\bcbs\\'

def process_single_formulary(doc, pdf_file, start_page, end_page):    
    drug_type = str()
    output_name = str(pdf_file).split('.')[0]
    formulary_df = pd.DataFrame(columns=['drug_type', 'drug_name', 'drug_tier', 'requirements_limits'])
    
    for page in doc:
        page_number = int(str(page).split(' ')[1])

        if page_number >= start_page and page_number <= end_page:
            tabs = page.find_tables()
            tab = tabs[0]
            
            for line in tab.extract():
                if 'Drug Tier' not in line:
                    if None in line:
                        drug_type = line[0]

                    line.insert(0, drug_type)
                    formulary_df.loc[len(formulary_df)] = line

    formulary_df = formulary_df.dropna()
    formulary_df.to_excel(output_path + '{}.xlsx'.format(output_name), index=False)

def main():
    pdf_list = common_func.get_pdf_list(input_path)
    for pdf_file in pdf_list:
        doc = common_func.read_pdf_fitz(input_path, pdf_file)       
        start_page, end_page = common_func.get_page_to_process_fitz(doc)
        process_single_formulary(doc, pdf_file, start_page, end_page)        

if __name__ == "__main__":
    main()
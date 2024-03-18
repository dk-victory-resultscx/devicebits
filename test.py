import pdfplumber

pdf_file = 'sample.pdf'

pdf_file_name = str(pdf_file).split('.')[0]
pdf = pdfplumber.open(pdf_file)

for page in pdf.pages:
    if page.page_number < 3:
        bounding_box = (0, 0, 550, 720)
        crop_area = page.within_bbox(bounding_box)
        content = crop_area.extract_text(
                                    x_tolerance=1
                                    ,y_tolerance=3
                                    ,layout=False
                                    )
    else:
        if page.page_number in (3, 4):
            bounding_box = (0, 0, 550, 720)
            crop_area = page.within_bbox(bounding_box)
            content = crop_area.extract_text(
                                        x_tolerance=1
                                        ,y_tolerance=3
                                        ,layout=False
                                        )

        elif page.page_number == 5:
            table = page.extract_table()
            if table:
                for data in table:
                    print(data)
from pdfquery import PDFQuery

pdf = PDFQuery('NHO.pdf')
pdf.load()
pdf.tree.write('customers.xml', pretty_print = True)

customer_name = pdf.pq('LTTextLineHorizontal:in_bbox("0, 0, 841.89, 595.28")').text()
print(customer_name)
import fitz # imports the pymupdf library

doc = fitz.open("a.pdf") # open a document

for page in doc: # iterate the document pages
    texts = page.get_text() # get plain text encoded as UTF-8
    texts = texts.strip()

    for text in texts.splitlines():
        if text != ' ':
            print(' '.join(text.split()))


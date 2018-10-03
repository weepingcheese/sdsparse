import os
import sys
import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    pages = PDFPage.get_pages(
        fp, pagenos, maxpages=maxpages, password=password,
        caching=caching, check_extractable=True)

    for page in pages:
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()

    return text


if __name__ == '__main__':
    pdfname = sys.argv[1]
    text = convert_pdf_to_txt(pdfname)
    outname = os.path.splitext(os.path.basename(pdfname))[0] + '.txt'
    with open(outname, 'w') as f:
        f.write(text)

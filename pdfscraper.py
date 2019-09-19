#!/usr/bin/env python3

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
from os import listdir
from os.path import isfile, join
import sys, getopt
import re
import argparse

def convert_pdf(fname, pages=None): # pdfminer
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = "utf-8"
    laparams = LAParams(all_texts=True, detect_vertical=False,
                        line_overlap=0.5, char_margin=2.0, line_margin=0.5,
                        word_margin=0.1, boxes_flow=0.5) # layout analysis
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    infile = open(fname, "rb")

    for page in PDFPage.get_pages(infile, pagenums, check_extractable=False):
        interpreter.process_page(page)
    infile.close()
    device.close()
    message = retstr.getvalue()
    retstr.close

    return message

def convert_pdf_ocr(fname): # pytesseract for ocr support
    
    pages = convert_from_path(fname, 500)
    image_counter = 1
    
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1
    
    totpages = image_counter - 1
    message = ""    
    for image in range(1, totpages + 1):
        filename = "page_" + str(image) + ".jpg"
        message += str((pytesseract.image_to_string(Image.open(filename))))
    
    return message

def txt_process(in_pdf, out_txt, token=None): # process text
   
   message = ""   
   for pdf in os.listdir(in_pdf):
        fileExtension = pdf.split(".")[-1]
        if fileExtension == "pdf":
            pdfFile = in_pdf + "/" +  pdf
            # try pdfminer
            message = convert_pdf(pdfFile)
            # if pdfminer returns blank string then try pytesseract
            if not message.strip():
                message = convert_pdf_ocr(pdfFile)
            # select regex for tokenization or standard text 
            if token:
                message = re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", message)
                message = " ".join(str(e) for e in message)
                message = message.lower()
            else:
            	message = re.findall(r"\w+(?:['-/]\w+)|\w+[?!.,:)(]|\S\w*", message)
            	message = " ".join(str(e) for e in message)
            txtFile = out_txt + "/" +  pdf + ".txt"
            txtFile = open(txtFile, "w")
            txtFile.write(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-dir", dest="inpdf", required=True, 
                        help="Path to the input pdf files")
    parser.add_argument("-o", "--output-dir", dest="outtxt", required=True,
                        help="Path for the output txt files")
    parser.add_argument("-t", "--token-gen", dest="token", action="store_true",
                        help="Use flag to generate tokenized output")

    args = parser.parse_args()

    in_pdf = args.inpdf
    out_txt = args.outtxt
    token = args.token

    txt_process(in_pdf, out_txt, token)

if __name__ == "__main__":
    main()


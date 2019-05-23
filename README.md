# **PDFscraper**


PDFscraper uses [PDFMiner](https://github.com/pdfminer/pdfminer.six) and [Python Tesseract](https://github.com/madmaze/pytesseract) to text mine pdfs.


## **Requirements**

PDFscraper requires python 3.x

The following python packages are prerequisites:
- pdfminer.six
- pytesseract
- chardet
- Python Imaging Library (PIL) or Pillow
- pdf2image


Other requirements:
Install of [Google Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [Poppler](https://github.com/danigm/poppler)

## **Usage**
```
usage: pdfscraper.py [-h] [-i INPDF] [-o OUTTXT]

optional arguments:
  -h, --help            show this help message and exit
  -i INPDF, --input-dir INPDF
                        Path to the input pdf files
  -o OUTTXT, --output-dir OUTTXT
                        Path for the output txt files
```


E.g. To run
```
python pdfscraper.py -i /path/to/input/pdfs/ -o /path/to/output/directory/
```

## **Docker**
Alternatively, the accompanying Dockerfile can be used to run the program in a docker container.

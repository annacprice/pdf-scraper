FROM python:3.6-alpine

COPY pdfscraper.py /app

WORKDIR /app

RUN apk update --no-cache && apk upgrade --no-cache && apk add --update --no-cache 

RUN apk add --no-cache --update build-base &&\
apk add --no-cache poppler-utils tesseract-ocr jpeg-dev zlib-dev

RUN pip3 install --no-cache-dir pdfminer.six &&\
pip3 install --no-cache-dir chardet &&\
pip3 install --no-cache-dir pillow &&\
pip3 install --no-cache-dir pytesseract &&\
pip3 install --no-cache-dir pdf2image 
 
RUN apk del build-base 

ENTRYPOINT ["python", "pdfscraper.py"]

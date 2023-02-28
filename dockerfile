FROM python:3.9

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /usr/src/app/script

CMD ["python", "kanji_dict_xml.py"]
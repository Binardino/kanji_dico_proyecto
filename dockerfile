FROM python:3.9

WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "script/kanji_dict_xml.py"]
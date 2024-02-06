FROM python:3.9-slim

LABEL authors="Anatoliy_Redko"

WORKDIR /usr/src/dataservice


COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]

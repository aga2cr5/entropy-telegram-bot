FROM python:3.8.10

ADD bot.py .

RUN pip install -r requirements.txt

CMD ["python", "./bot.py"]

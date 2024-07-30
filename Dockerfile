FROM python:3.11

RUN mkdir /fastapi_app
WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python -m src.api.main
CMD python -m src.bot.main

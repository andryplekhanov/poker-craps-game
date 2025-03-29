FROM python:3.10-slim-buster

ENV BOT_NAME=$BOT_NAME

WORKDIR /app/$BOT_NAME

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip  \
    && pip install --no-cache-dir -r ./requirements.txt

COPY . .

CMD ["python", "bot.py"]

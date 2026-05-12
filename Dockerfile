FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt


RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
FROM python:latest

COPY . .

RUN pip install --no-cache-dir requirements.txt

CMD [ "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000" ]
FROM python:3.11-slim

WORKDIR /server

RUN pip install --no-cache-dir flask

COPY servidor.py /server/servidor.py

EXPOSE 5000

CMD ["python", "servidor.py"]
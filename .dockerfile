FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG en_GB.UTF-8
ENV PYTHONIOENCODING utf_8

RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "entrypoint.py"]

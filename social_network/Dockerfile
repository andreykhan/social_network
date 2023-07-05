FROM python:3.7-slim
RUN mkdir /app
COPY /social_network/requirements.txt /app
RUN pip install -r /app/requirements.txt --no-cache-dir
COPY . /app
WORKDIR /app
CMD ["gunicorn", "social_network.wsgi:application", "--bind", "0:8000" ] 
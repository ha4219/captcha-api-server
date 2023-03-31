FROM python:3.10

EXPOSE 8000

WORKDIR /code

RUN apt-get update
RUN apt-get install libgl1-mesa-glx -y

COPY . /code

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

#  uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 8000
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "300"]
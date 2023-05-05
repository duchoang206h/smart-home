#
FROM --platform=linux/amd64 python:3.10

USER root
#
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir
#
#COPY Pipfile Pipfile.lock /code/
COPY ./ /code/

#
#RUN pip install mysqlclient
#&& pipenv install --system


#

#
#CMD ["pipenv", "run", "./venv/bin/activate","python3", "main.py"]
#RUN pipenv run ./venv/bin/activate python3 main.py
CMD uvicorn main:app --host 0.0.0.0 --port 8000
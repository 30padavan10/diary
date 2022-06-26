FROM python:3.9
#RUN pip install pipenv
#RUN mkdir /code
WORKDIR /code
#COPY Pipfile* /code/
#RUN pipenv install --deploy --ignore-pipfile
COPY . /code
RUN pip install -r requirements.txt
#ADD sec /code/
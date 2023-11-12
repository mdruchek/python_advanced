FROM python:3.12-slim

RUN mkdir /new_year_application

COPY requirements.txt /new_year_application/

RUN python -m pip install -r /new_year_application/requirements.txt

COPY static/ /new_year_application/static/

COPY templates/ /new_year_application/templates/

COPY app.py /new_year_application/

WORKDIR /new_year_application

ENTRYPOINT ["python", "app.py"]
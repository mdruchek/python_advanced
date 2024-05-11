FROM python:3.10-alpine
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./my_proj ./my_proj
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "my_proj:create_app()"]
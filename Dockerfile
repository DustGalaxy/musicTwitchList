FROM python:3.12

#
WORKDIR /code

#
RUN pip install poetry

#
COPY ./pyproject.toml ./poetry.lock* /code/

#
RUN poetry install

#
COPY ./bot_config.json /code/
COPY ./src /code/src
COPY .env /code/

#
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

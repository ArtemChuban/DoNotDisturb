FROM python:3.11-alpine
WORKDIR /code
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root
COPY . .
CMD ["poetry", "run", "python", "app/main.py"]

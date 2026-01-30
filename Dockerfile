FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN poetry install --only main --no-root

COPY . .

EXPOSE 8000
CMD ["poetry", "run", "start"]
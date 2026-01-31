FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock* README.md ./

RUN uv sync --frozen --no-dev --no-cache

COPY . .

ENV PYTHONPATH="/app:/app/src"

EXPOSE 8000

CMD ["uv", "run", "python", "main.py"]

FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

COPY . .

RUN uv sync

CMD ["uv", "run", "fastapi", "run", "app.py"]
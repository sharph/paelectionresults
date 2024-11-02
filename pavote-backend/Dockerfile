FROM python:slim

RUN pip install uv

WORKDIR /app
COPY README.md requirements.lock pyproject.toml ./
RUN uv pip install --no-cache --system -r requirements.lock

COPY src/pavote_backend/* ./
CMD fastapi run

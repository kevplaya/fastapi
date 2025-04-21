FROM python:3.13.3

# Configure python
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
ENV PYTHONUNBUFFERED 1

# Update utilities
RUN apt-get update
RUN apt-get install default-mysql-client -y

# Poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /wanted

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

COPY . .

CMD ["gunicorn", "main:app", "--workers=4", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]

FROM python:3.13

WORKDIR /smartcms
ENV PYTHONPATH=/smartcms

RUN pip install uv
COPY uv.lock pyproject.toml ./
RUN uv sync --no-dev

COPY . .

# CMD [ "uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0","--reload"]
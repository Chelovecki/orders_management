FROM python:3.13

WORKDIR /order_management
ENV PYTHONPATH=/order_management

RUN pip install uv
COPY uv.lock pyproject.toml ./
RUN uv sync --no-dev

COPY . .

# Добавляем entrypoint
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
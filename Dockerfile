FROM python:3.13-slim

ENV exe="BUMPY"
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Install pipx and poetry in one layer, clean up cache
RUN pip install --no-cache-dir pipx && \
    pipx install poetry && \
    rm -rf /root/.cache

# Copy only dependency files first for better layer caching
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy application code
COPY frontend_app.py backend_app.py create_envs.py /app/

EXPOSE 8080

CMD ["sh", "-c", "python $exe"]
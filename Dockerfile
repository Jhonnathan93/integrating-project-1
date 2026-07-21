# python:3.14-slim
FROM python@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6

ARG SOURCE_URL
ARG VCS_REF

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

LABEL org.opencontainers.image.source=$SOURCE_URL \
    org.opencontainers.image.revision=$VCS_REF \
    org.opencontainers.image.title="BookNexus"

WORKDIR /app

COPY requirements.lock ./
RUN pip install --no-cache-dir --only-binary=:all: --require-hashes --requirement requirements.lock

# Copy only the runtime source. Build metadata, local environments, and secret
# files are intentionally excluded from the image (also enforced by .dockerignore).
COPY manage.py ./
COPY BookNexus/ ./BookNexus/
COPY accounts/ ./accounts/
COPY analytics/ ./analytics/
COPY book/ ./book/
COPY newsletter/ ./newsletter/
COPY readinglists/ ./readinglists/
COPY reports/ ./reports/
COPY static/ ./static/

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/', timeout=3)" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "BookNexus.wsgi:application"]

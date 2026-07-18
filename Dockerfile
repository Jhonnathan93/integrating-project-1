FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.lock ./
RUN pip install --no-cache-dir --only-binary=:all: pip==26.1.2 \
    && pip install --no-cache-dir --only-binary=:all: --requirement requirements.lock

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

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "BookNexus.wsgi:application"]

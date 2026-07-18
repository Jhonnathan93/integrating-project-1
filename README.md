# BookNexus

A Django web application for discovering books, receiving recommendations, and
organizing personal reading lists.

## Features

- Recommendations based on preferences and reference books.
- Book metadata retrieval through Google Books.
- Private reading lists, including a default list.
- User profiles and disliked-book tracking.
- Book analytics and staff-only reports.
- Staff-restricted newsletter delivery.

## Architecture

Each Django application separates responsibilities:

| Layer | Responsibility |
| --- | --- |
| `views.py` | Receives HTTP requests, validates input, and returns responses. |
| `services.py` | Performs state changes, domain validation, and transactions. |
| `selectors.py` | Centralizes database queries and read operations. |
| `models.py` | Defines data structures and simple entity-level rules. |

External integrations live in dedicated modules, such as
`book/google_books.py`. This structure keeps business logic out of views and
makes it reusable from commands, tasks, and tests.

## Requirements

- Python 3.14
- pip
- Git
- Docker, optionally, to build the application image

Check the active Python version:

```powershell
python --version
```

## Local setup

1. Clone the repository and enter its directory:

   ```powershell
   git clone https://github.com/Jhonnathan93/integrating-project-1.git
   cd integrating-project-1
   ```

2. Create and activate a Python 3.14 virtual environment:

   ```powershell
   py -3.14 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install application dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` in the project root and fill in the values. This file must not be committed:

   ```powershell
   Copy-Item .env.example .env
   ```

   ```dotenv
   DJANGO_SECRET_KEY=a-secure-development-only-secret
   DJANGO_DEBUG=true
   GOOGLE_BOOKS_API_KEY=
   LLM_PROVIDER=groq
   GROQ_API_KEY=
   GROQ_MODEL=llama-3.3-70b-versatile
   OPENAI_API_KEY=
   OPENAI_MODEL=gpt-5.4-mini
   NEWSLETTER_SENDER_EMAIL=
   NEWSLETTER_SENDER_PASSWORD=
   ```

   Google Books, the configured LLM provider (`groq` or `openai`), and newsletter
   credentials are optional to start the application, but required for their
   respective features.

5. Apply migrations and start the development server:

   ```powershell
   python manage.py migrate
   python manage.py runserver
   ```

Open <http://127.0.0.1:8000/>.

## Development and quality checks

Install development tools once:

```powershell
python -m pip install --require-hashes -r requirements-dev.lock
```

| Goal | Command |
| --- | --- |
| Django system check | `python manage.py check` |
| Pending migrations | `python manage.py makemigrations --check --dry-run` |
| Fast linting | `python -m ruff check .` |
| Format with Ruff | `python -m ruff format .` |
| Type checking | `python -m mypy --config-file mypy.ini --ignore-missing-imports accounts analytics book newsletter readinglists reports BookNexus` |
| Static security analysis | `python -m semgrep scan --config p/python --config p/django --error` |
| Dependency vulnerability scan | `python -m pip_audit -r requirements.lock` |
| Unit tests | `python manage.py test --settings=BookNexus.settings_test` |
| Coverage check (minimum 85%) | `python -m coverage run --branch manage.py test --settings=BookNexus.settings_test; python -m coverage report --fail-under=85` |
| HTML and XML coverage reports | `python -m coverage html; python -m coverage xml` |

## Docker

Build the local image:

```powershell
docker build -t booknexus:local .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 --env-file .env booknexus:local
```

The image uses Gunicorn and exposes port 8000. In a real deployment, configure
a persistent database and production environment variables.

## CI/CD

The GitHub Actions workflow in
[.github/workflows/ci.yml](.github/workflows/ci.yml) runs for every pull
request targeting `main` and every push to `main`.

It includes:

- Line-ending and Conventional Commit message validation.
- Ruff and mypy.
- Semgrep, Gitleaks, dependency audit, and license checks.
- Migration validation and application against a clean SQLite database.
- Python compilation, Docker image build, and image vulnerability scanning.
- Final publication of source and license artifacts in GitHub Actions.

For external failure notifications, configure the optional
`FAILURE_WEBHOOK_URL` repository secret.

## Conventions

- Do not commit `.env`, SQLite databases, `media/`, or virtual
  environments.
- Migrations are part of the codebase and must accompany every model change.
- Database writes belong in a service.
- Reusable queries belong in a selector.
- Commits follow Conventional Commits and include a non-empty description.

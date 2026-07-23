# BookNexus

<p align="center">
  <img src="static/img/book_logo.png" alt="BookNexus logo" width="220">
</p>

<p align="center">
  A Django platform for discovering books, receiving personalized recommendations, and organizing reading lists.
</p>

## Table of contents

- [About](#about)
- [Features](#features)
- [Usage](#usage)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Commands](#commands)
- [Architecture](#architecture)
- [Testing and quality](#testing-and-quality)
- [Docker and deployment](#docker-and-deployment)
- [CI/CD](#cicd)
- [Contributing](#contributing)
- [Branches](#branches)
- [FAQ](#faq)
- [Resources](#resources)
- [Gallery](#gallery)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## About

BookNexus is a web application that helps readers discover and engage with books.
It combines reading preferences, history, and interests to generate personalized
recommendations, while providing book metadata such as authors, descriptions,
genres, and publication details.

The project is motivated by the social and individual value of reading. By making
book discovery more approachable and personal, BookNexus aims to support a more
informed, connected community of readers.

## Features

- Personalized recommendations based on selected books, preferences, and interests.
- Configurable Groq or OpenAI recommendation providers.
- Google Books metadata lookup with resilient error handling.
- User accounts, profiles, disliked-book tracking, and reading history.
- Private reading lists, including a default read-later list.
- Book rankings and staff-only reading reports.
- Staff-restricted newsletter delivery.
- Responsive interface for desktop and mobile devices.

## Usage

1. Create an account and complete your reader profile.
2. Select reference books and your reading interests on the home page.
3. Request recommendations and explore the book information returned.
4. Save books to a reading list or mark titles as not recommended.
5. Review your profile, lists, and rankings. Staff users can access reports and
   newsletter delivery.

## Prerequisites

- Python 3.14
- pip
- Git
- Docker Engine, optional for image builds and container-based runs
- API keys, optional for external features:
  - Google Books API
  - Groq or OpenAI
  - SMTP credentials for newsletter delivery

Verify the active interpreter before installing dependencies:

```powershell
python --version
```

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Jhonnathan93/integrating-project-1.git
cd integrating-project-1
```

Create and activate a Python 3.14 virtual environment.

**Windows PowerShell**

```powershell
py -3.14 -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS and Linux**

```bash
python3.14 -m venv venv
source venv/bin/activate
```

Install runtime dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For reproducible development tooling, install the locked development dependencies:

```bash
python -m pip install --require-hashes -r requirements-dev.lock
```

## Configuration

Create a local environment file from the example:

```powershell
Copy-Item .env.example .env
```

```bash
cp .env.example .env
```

Configure the values required by your environment:

| Variable | Purpose | Required locally |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Django cryptographic key | Yes |
| `DJANGO_DEBUG` | Enables development mode | Yes |
| `DJANGO_ALLOWED_HOSTS` | Hosts allowed when debug is disabled | Production only |
| `ALLOWED_HOSTS` | Alternative name accepted for deployment hosts | Production only |
| `CSRF_TRUSTED_ORIGINS` | HTTPS origins trusted for POST requests | Production only |
| `DATABASE_URL` | PostgreSQL connection URI; uses local SQLite when omitted | Production only |
| `LLM_PROVIDER` | `groq` or `openai` | For recommendations |
| `GROQ_API_KEY` / `OPENAI_API_KEY` | Credentials for the selected LLM provider | For recommendations |
| `GOOGLE_BOOKS_API_KEY` | Google Books API credential | For book metadata |
| `NEWSLETTER_SENDER_EMAIL` | Newsletter sender address | For newsletter delivery |
| `NEWSLETTER_SENDER_PASSWORD` | Newsletter sender password or app password | For newsletter delivery |

Never commit `.env`, local databases, uploaded media, or credentials.

### Supabase PostgreSQL

For a Supabase-backed deployment, open **Connect** in the Supabase dashboard and
copy the **Transaction pooler** URI (port `6543`) into `DATABASE_URL`. This
pooler is intended for transient serverless connections such as Vercel. Keep a
direct connection URI only for migrations and administration tools.

Apply the Django migrations once against the Supabase database:

```bash
python manage.py migrate
python manage.py createsuperuser
```

The dedicated test settings always use in-memory SQLite, even when your local
`.env` contains `DATABASE_URL`.

Apply migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Commands

| Goal | Command |
| --- | --- |
| Django system check | `python manage.py check` |
| Pending migrations | `python manage.py makemigrations --check --dry-run` |
| Apply migrations | `python manage.py migrate` |
| Lint | `python -m ruff check .` |
| Check formatting | `python -m ruff format --check .` |
| Format code | `python -m ruff format .` |
| Type check | `python -m mypy --config-file mypy.ini --ignore-missing-imports accounts analytics book newsletter readinglists reports BookNexus` |
| Validate YAML | `git ls-files -z -- '*.yaml' '*.yml' ':!.yamllint.yml' \| xargs -0 yamllint` |
| SAST | `python -m semgrep scan --config p/python --config p/django --error` |
| Dependency audit | `python -m pip_audit -r requirements.lock` |
| Unit tests | `python manage.py test --settings=BookNexus.settings_testing --exclude-tag=integration` |
| Integration tests | `python manage.py test --settings=BookNexus.settings_testing --tag=integration` |
| Coverage threshold | `python -m coverage run --branch manage.py test --settings=BookNexus.settings_testing --exclude-tag=integration; python -m coverage report --fail-under=85` |
| Coverage reports | `python -m coverage html; python -m coverage xml` |

## Architecture

The Django apps separate HTTP handling, business operations, and query logic:

| Layer | Responsibility |
| --- | --- |
| `views.py` | Handles HTTP requests and responses. |
| `services.py` | Performs writes, validation, and transactional business operations. |
| `selectors.py` | Centralizes read-only queries. |
| `models.py` | Defines persisted data and entity-level behavior. |
| `urls.py` | Defines routes owned by each app. |

External providers are isolated in modules such as `book/google_books.py` and
`book/llm_providers.py`, making them easier to mock and replace.

```text
BookNexus/                 Project settings, infrastructure routes, ASGI/WSGI
accounts/                  Authentication and reader profiles
analytics/                 Book rankings and periods
book/                      Recommendations, providers, metadata, and history
newsletter/                Newsletter delivery
readinglists/              Reading-list domain and views
reports/                   Staff reading reports and chart data
static/                    Shared styles, scripts, images, and vendor assets
.github/workflows/ci.yml   Continuous integration and delivery workflow
```

## Testing and quality

The project uses Django's native test runner. Unit tests are isolated and quick;
integration tests carry the `integration` tag and mock external boundaries such
as Google Books, LLM providers, and SMTP.

Coverage runs with branch measurement and requires at least **85%** for unit
tests. HTML and XML reports are generated for local review and SonarCloud.

Code quality also includes Ruff, mypy, Semgrep, Gitleaks, `pip-audit`, license
checks, configuration validation, and migration checks.

## Docker and deployment

Build the image:

```bash
docker build -t booknexus:local .
```

Run it with local environment values:

```bash
docker run --rm -p 8000:8000 --env-file .env booknexus:local
```

The image runs Gunicorn as a non-root user and exposes port `8000`. It includes a
health endpoint at `/health/`. A production deployment should provide persistent
database storage, production environment variables, and a migration strategy.

## CI/CD

The GitHub Actions workflow in [`.github/workflows/ci.yml`](.github/workflows/ci.yml)
runs on pushes and pull requests targeting `main`.

It validates formatting, commits, configuration, types, security, dependencies,
migrations, unit and integration tests, coverage, SonarCloud quality gates, and
the Docker image. The pipeline scans the filesystem and built image, verifies
the container health endpoint, publishes the image to GitHub Container Registry,
and generates a provenance attestation for the published image digest.

The workflow publishes source, coverage, and license reports as GitHub Actions
artifacts. Configure the optional `FAILURE_WEBHOOK_URL` repository secret to
receive external failure notifications.

## Contributing

Contributions are welcome.

1. Open an issue for bugs or feature proposals when discussion is useful.
2. Create a focused branch from the current target branch.
3. Keep views thin: put writes in services and reusable reads in selectors.
4. Add or update tests for changed behavior.
5. Run the relevant commands in [Commands](#commands).
6. Use Conventional Commits with a non-empty body.
7. Open a pull request and address review feedback.

Pull requests must pass the required CI checks. Do not commit secrets, local
artifacts, generated media, or database files.

## Branches

- `main` is protected and receives changes through pull requests after required
  checks pass.
- `development` can be used as the shared integration branch when a staging
  branch is needed.
- Use short-lived branches such as `feat/<topic>`, `fix/<topic>`, or
  `chore/<topic>` for focused work.

Rebase a working branch on its target before merging when a linear history is
required. Prefer `git push --force-with-lease` over `--force` after a rebase.

## FAQ

### Do I need external API keys to run BookNexus?

No. The application starts without them, but recommendation, metadata, and
newsletter features need their corresponding credentials.

### Is BookNexus a public API?

No. It is a server-rendered Django application; it does not currently expose a
documented public API.

### Why do tests use `BookNexus.settings_testing`?

The dedicated settings module isolates tests from `.env`, uses an in-memory mail
backend, temporary media storage, fast password hashing, and empty external keys.

## Resources

- [Django documentation](https://docs.djangoproject.com/)
- [GitHub Actions workflow](.github/workflows/ci.yml)
- [Google Books API](https://developers.google.com/books)
- [Groq API documentation](https://console.groq.com/docs/overview)
- [OpenAI API documentation](https://platform.openai.com/docs/)

## Gallery

The application interface includes book recommendations, reading lists, reader
profiles, rankings, and staff reports. Add maintained screenshots under
`docs/images/` and reference them here when visual documentation is available.


## License

No license file is currently included in this repository. Do not assume reuse,
redistribution, or modification rights until a license is added.

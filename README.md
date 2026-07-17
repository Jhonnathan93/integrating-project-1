<h1 align="center">BookNexus </h1>

> Empowering users to make informed decisions about their reading choices.




# General Information

Booknexus is a web-based book recommendation application that offers personalized suggestions based on users' preferences, and provides information about various books, including author details, synopses, and genres.

This project also includes data analytics.

# Requirements

Make sure you have Python installed:

- [Python](https://www.python.org/downloads/): Programming language used in the project.

Install the project dependencies:

 ```bash
python -m pip install -r requirements.txt
 ```

# Instructions to run the program

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/Jhonnathan93/integrating-project-1.git
    ```

2. Navigate to the project directory:

    ```bash
    cd integrating-project-1
    ```

3. Perform database migrations:

    ```bash
    python manage.py migrate
    ```

   Configure secrets in `keys.env` (never commit this file). The supported names are
   `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `GOOGLE_BOOKS_API_KEY`, `OPENAI_API_KEY`,
   `NEWSLETTER_SENDER_EMAIL`, and `NEWSLETTER_SENDER_PASSWORD`.

4. Start the development server:

    ```bash
    python manage.py runserver
    ```

5. Open your web browser and visit [http://localhost:8000/](http://localhost:8000/) to see the application running.

# Architecture

The domain code follows a service/selector split:

- `services.py` contains transactional state changes and validation.
- `selectors.py` contains database reads and query optimization.
- `views.py` is the HTTP layer only: it validates input, calls a service or selector, and returns a response.
- External integrations live behind dedicated modules such as `book/google_books.py`.

This keeps business rules reusable from views, tasks, commands, and tests while making side effects explicit.







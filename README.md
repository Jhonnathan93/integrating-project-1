<h1 align="center">BookNexus</h1>

# General Information
Project for the course Integrating Project 1 (ST0251) - EAFIT University.

Booknexus is a web-based application that aims to let users discover and engage with books. It is a book recommendation application that offers personalized suggestions based on users' preferences, reading history, and interests. Additionally, the application provides comprehensive information about various books, including author details, synopses, and genres. Empowering users to make informed decisions about their reading choices.

# Requirements of the project
Before running this program, make sure you have the following libraries and dependencies installed:

**pip**: pip is Python's package management system and is generally included with the installation of Python from version 3.0 onwards. It is used to install, update, and manage third-party libraries and dependencies. Pip is required in this project to install the specific libraries and dependencies that make the application work.

**Django**: This project uses the Django framework. Django is a high-level web development framework that makes it easy to create robust and scalable web applications. We need Django to build and run the web application for this project. To install Django, we use pip, since pip allows us to install Python libraries from the PyPI (Python Package Index) repository:

 ```bash
 pip install Django
 ```

**OpenAI Python SDK**: This project uses the Python library provided by OpenAI to interact with its API. OpenAI is an artificial intelligence platform that provides natural language processing (NLP) services. OpenAI's Python library allows us to make requests to its API and get responses which we use in this project.

 ```bash
pip install openai
 ```

**requests**: The requests library is a Python library used to make HTTP requests. In this project, we use requests to make requests to the Google Books API and get information about books based on user queries.

 ```bash
pip install requests
 ```


# Instructions to run the program

Below are the steps to set up and run this project on your local device.

### Previous requirements

Make sure you have the components mentioned above installed in addition to:

- [Python](https://www.python.org/downloads/): Programming language used in the project.

### Installation instructions

1. Clone this repository to your local machine:

    ```bash
    git clone --single-branch --branch sprint2 https://github.com/Jhonnathan93/integrating-project-1.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-project
    ```

3. Perform database migrations:

    ```bash
    python manage.py migrate
    ```

4. Start the development server:

    ```bash
    python manage.py runserver
    ```

5. Open your web browser and visit [http://localhost:8000/](http://localhost:8000/) to see the application running.







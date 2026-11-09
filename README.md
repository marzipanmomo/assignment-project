# Aurora Decor

A full-stack e-commerce website selling home decor and furniture, built with Django and PostgreSQL. It has user authentication (sign up, log in, log out), a product catalogue with categories, a contact form, and containerised deployment with Docker.

## Run locally

Requires Python 3.10+ and a PostgreSQL server with an empty database (e.g. 'assignment_db').

1. Create and activate a virtual environment
    'python -m venv venv' then 'venv\Scripts\activate'
2. Install dependencies 'pip install -r requirements.txt'
3. Move into the backend folder: 'cd backend'
4. Create the tables: 'python manage.py migrate'
5. Load the products and categories: 'python manage.py import_products'
6. Start the server: 'python manage.py runserver'
7. Open http://127.0.0.1:8000/ and sign up for an account

## Run with Docker

Requires Docker Desktop to be running.

1. Copy 'backend/.env.example' to 'backend/.env' and fill in your own values.
2. From the project root: 'docker compose --env-file backend/.env up --build' This starts PostgreSQL, applies migrations annd imports the products automatically.
3. Open http://localhost:8000/ and sign up for an account.
4. (Optional) Create an admin user for '/admin/': 'docker compose --env-file backend/.env exec web python manage.py createsuperuser'

## Features
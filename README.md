# FoodConnect

FoodConnect is a simple Django web application that connects food donors with receivers. Donors can publish food listings, receivers can claim them, and both roles get a dashboard to manage their activity.

## Features

- User authentication with donor and receiver roles
- Food listing create, browse, and delete flows
- Food claim system for receivers
- Dashboard with personal listings and claims
- Clean HTML and CSS with SQLite for easy local setup

## Run the project

1. Create and activate a virtual environment if you want an isolated setup.
2. Install Django if it is not already available:

```bash
pip install django
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Create an admin user if needed:

```bash
python manage.py createsuperuser
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Open `http://127.0.0.1:8000/`

## Apps

- `accounts`: custom user model, signup, login, dashboard
- `food`: food listing, claim, and homepage features

# Bandhan Django E-commerce

Bandhan is a Django 5.2 LTS-ready fashion e-commerce application using Django templates, HTMX, Alpine.js, Tailwind CSS, server-side cart/checkout logic, paisa integer money storage, and a custom email-login user model.

## Quick Start

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
npm install
npm run css:build
python manage.py migrate
python manage.py seed_demo_data
python manage.py import_demo_products
python manage.py createsuperuser
python manage.py runserver
```

Use `DATABASE_URL` to select PostgreSQL or MySQL:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/bandhan
DATABASE_URL=mysql://user:password@localhost:3306/bandhan
```

Compiled `static/css/app.css` is committed so production hosting does not need Node.js to serve requests.

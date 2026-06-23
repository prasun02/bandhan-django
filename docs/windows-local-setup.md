# Windows Local Setup

Use Python 3.12, create a virtual environment, install requirements, build CSS, migrate, seed data, import products, and run the development server.

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
npm install
npm run css:build
python manage.py migrate
python manage.py seed_demo_data
python manage.py import_demo_products
python manage.py runserver
```

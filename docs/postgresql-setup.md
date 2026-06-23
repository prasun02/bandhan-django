# PostgreSQL Setup

Create a database and user, then set:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/bandhan
```

Run `python manage.py migrate` after installing `psycopg[binary]`.

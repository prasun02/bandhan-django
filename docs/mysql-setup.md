# MySQL Setup

Create a UTF-8 database and user, then set:

```env
DATABASE_URL=mysql://user:password@localhost:3306/bandhan
```

Use `utf8mb4` and run `python manage.py migrate` after installing `mysqlclient`.

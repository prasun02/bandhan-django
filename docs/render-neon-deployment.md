# Render and Neon Free Demo Deployment

1. Create a free Neon PostgreSQL project.
2. Copy the pooled PostgreSQL connection URL.
3. Push this project to GitHub.
4. Create a Render Web Service.
5. Connect the GitHub repository.
6. Select the Free instance type.
7. Set the build command: `bash build.sh`.
8. Set the start command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`.
9. Add environment variables.
10. Deploy.
11. Verify the homepage.
12. Verify `/admin/`.
13. Verify `/static/css/app.css` returns HTTP 200.
14. Verify product data.
15. Verify checkout.
16. Verify order creation.
17. Verify database persistence.

Required Render environment variables:

```env
SECRET_KEY=replace-with-long-random-secret
DEBUG=False
ALLOWED_HOSTS=your-service.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-service.onrender.com
DATABASE_URL=postgresql://...
TIME_ZONE=Asia/Dhaka
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=replace-with-strong-password
DJANGO_SUPERUSER_FULL_NAME=Bandhan Admin
```

Do not commit real credentials, Neon URLs, payment keys, or customer uploads. Render's free filesystem is temporary, so admin-uploaded media needs external storage such as Cloudflare R2, S3, or Cloudinary for production permanence.

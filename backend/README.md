# Arcnoids API

Django REST Framework backend for the internal Arcnoids workspace.

## Implemented scope
- Individual username/password accounts; no public registration.
- Workspace roles: ADMIN, MANAGER, EMPLOYEE.
- Admin-only team account creation/deactivation.
- Admin/manager access to clients and enquiries.
- Admin/manager project and task management.
- Employees see projects assigned to them and tasks assigned to them; employees can update task status only.
- Session authentication with CSRF protection.

## Local setup
1. Create a Python virtual environment and install `requirements.txt`.
2. Copy `.env.example` to `.env`; set a strong `DJANGO_SECRET_KEY`.
3. Export the variables from `.env` into your shell.
4. Run `python manage.py migrate`.
5. Run `python manage.py bootstrap_admin` once with ADMIN_USERNAME, ADMIN_EMAIL and ADMIN_PASSWORD set.
6. Run `python manage.py runserver`.

## API
- GET /api/health/
- GET /api/auth/csrf/ then POST /api/auth/login/
- POST /api/auth/logout/; GET /api/auth/me/
- POST /api/auth/password/
- GET/POST /api/team/ (admin only)
- GET/POST/PATCH/DELETE /api/clients/ (admin/manager)
- GET/POST/PATCH/DELETE /api/projects/ (admin/manager; employees can read assigned projects)
- GET/POST/PATCH/DELETE /api/tasks/ (admin/manager; employees see assigned tasks and can update status only)
- GET/POST/PATCH/DELETE /api/enquiries/ (admin/manager)

All endpoints except health, CSRF bootstrap, login and bootstrap-status require an authenticated session.

## Deploy
Deploy with the root-level Render blueprint. Set CORS_ALLOWED_ORIGINS and CSRF_TRUSTED_ORIGINS to the exact HTTPS frontend origin(s). Set ADMIN_EMAIL and ADMIN_PASSWORD as secret environment variables. The container startup runs migrations and the idempotent bootstrap_admin command before starting Gunicorn. Check the Render logs for the owner-created message.

Do not commit production secrets or a .env file. The bootstrap command will not overwrite an existing active admin.

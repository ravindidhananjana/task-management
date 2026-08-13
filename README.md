
````markdown
# Task Management REST API

A role-based Task Management REST API built with Django REST Framework and PostgreSQL.

## Features

- Django REST Framework
- PostgreSQL database
- Custom User model with Admin and Member roles
- JWT authentication
- Login, token refresh, and logout
- Role-based permissions
- Project CRUD operations
- Task CRUD operations
- Soft delete for Tasks
- Task assignment
- Pagination
- Search by title and description
- Filtering by status, priority, assigned user, and project
- Ordering by due date, creation date, and other task fields
- Automatic ActivityLog creation using Django signals
- Django Admin interface
- Automated API tests

## Technology Stack

- Python 3.11
- Django 5.2
- Django REST Framework
- PostgreSQL
- SimpleJWT
- django-filter

## Project Structure

```text
Task Manager/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   └── tests.py
│
├── projects/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── activity_logs/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── signals.py
│   └── tests.py
│
├── core/
│   ├── activity_context.py
│   └── permissions.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .env.example
├── .gitignore
├── manage.py
└── README.md
````

## Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Task-Manager
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Use `.env.example` as a template:

```text
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

Do not commit `.env` to GitHub.

### 5. Create the PostgreSQL database

Create a PostgreSQL database matching the values configured in `.env`.

### 6. Run migrations

```powershell
python manage.py migrate
```

### 7. Create a superuser

```powershell
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

### 8. Run the development server

```powershell
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Authentication

The API uses JWT authentication.

### Login

```text
POST /api/v1/auth/login/
```

Example request:

```json
{
    "username": "admin",
    "password": "your-password"
}
```

The response contains an access token and refresh token.

Use the access token for authenticated requests:

```text
Authorization: Bearer <access_token>
```

### Refresh Token

```text
POST /api/v1/auth/refresh/
```

### Logout

```text
POST /api/v1/auth/logout/
```

## Roles and Permissions

### Admin

Administrators can:

* Create Projects
* Update Projects
* Delete Projects
* Create Tasks
* Update Tasks
* Delete Tasks
* Manage resources through the API
* Access the Django Admin panel

### Member

Members can:

* Create Tasks
* View permitted resources
* Update Tasks assigned to themselves
* Cannot delete Tasks
* Cannot delete Projects
* Cannot modify Tasks assigned to other users

When a Member creates a Task, the Task is automatically assigned to that Member.

## API Endpoints

| Method | Endpoint                 | Description                             |
| ------ | ------------------------ | --------------------------------------- |
| POST   | `/api/v1/auth/login/`    | Obtain JWT access and refresh tokens    |
| POST   | `/api/v1/auth/refresh/`  | Refresh an access token                 |
| POST   | `/api/v1/auth/logout/`   | Logout and invalidate the refresh token |
| GET    | `/api/v1/projects/`      | List Projects                           |
| POST   | `/api/v1/projects/`      | Create a Project                        |
| GET    | `/api/v1/projects/{id}/` | Retrieve a Project                      |
| PATCH  | `/api/v1/projects/{id}/` | Update a Project                        |
| PUT    | `/api/v1/projects/{id}/` | Replace a Project                       |
| DELETE | `/api/v1/projects/{id}/` | Delete a Project                        |
| GET    | `/api/v1/tasks/`         | List Tasks                              |
| POST   | `/api/v1/tasks/`         | Create a Task                           |
| GET    | `/api/v1/tasks/{id}/`    | Retrieve a Task                         |
| PATCH  | `/api/v1/tasks/{id}/`    | Update a Task                           |
| PUT    | `/api/v1/tasks/{id}/`    | Replace a Task                          |
| DELETE | `/api/v1/tasks/{id}/`    | Soft-delete a Task                      |
| GET    | `/api/v1/activity-logs/` | View Activity Logs                      |

## Task List Features

### Pagination

Tasks are returned with 10 items per page.

Example:

```text
GET /api/v1/tasks/?page=2
```

### Search

Search by title or description:

```text
GET /api/v1/tasks/?search=meeting
```

### Filtering

Filter by status:

```text
GET /api/v1/tasks/?status=TODO
```

Filter by priority:

```text
GET /api/v1/tasks/?priority=HIGH
```

Filter by assigned user:

```text
GET /api/v1/tasks/?assigned_to=2
```

### Ordering

Order by due date:

```text
GET /api/v1/tasks/?ordering=due_date
```

Order by newest creation date:

```text
GET /api/v1/tasks/?ordering=-created_at
```

## Soft Delete

Tasks use soft deletion.

When a Task is deleted:

```text
is_deleted = True
```

The Task is therefore retained in the database but excluded from normal Task query results.

Only authorized Admin users can perform the delete operation.

## Activity Logging

CREATE, UPDATE, and DELETE operations on Projects and Tasks automatically create ActivityLog records.

Each ActivityLog contains:

* User
* Action
* Model name
* Object ID
* Timestamp

Activity logging is implemented using Django signals.

Example:

```text
CREATE Task #18
UPDATE Task #18
DELETE Task #18
```

## Testing

Run the complete test suite:

```powershell
python manage.py test
```

The project currently contains 7 automated tests covering authentication, permissions, task creation, soft deletion, and ActivityLog behavior.

Expected result:

```text
Ran 7 tests

OK
```

## Django Admin

The Django Admin interface is available at:

```text
http://127.0.0.1:8000/admin/
```

Administrators can manage:

* Users
* Projects
* Tasks
* Activity Logs

## Environment Variables

The following environment variables are required:

| Variable      | Description              |
| ------------- | ------------------------ |
| `SECRET_KEY`  | Django secret key        |
| `DEBUG`       | Django debug setting     |
| `DB_NAME`     | PostgreSQL database name |
| `DB_USER`     | PostgreSQL username      |
| `DB_PASSWORD` | PostgreSQL password      |
| `DB_HOST`     | PostgreSQL host          |
| `DB_PORT`     | PostgreSQL port          |

The actual `.env` file is excluded from version control.

## License

This project was developed as part of a Python Developer Intern skill assessment.






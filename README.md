# Enterprise Task API

A RESTful backend API for managing projects and tasks, built with Django REST Framework and PostgreSQL. The application provides JWT-based authentication and APIs for creating, retrieving, and updating projects and tasks.

## Features

- **JWT Authentication** — Secure API access using JSON Web Tokens.
- **Project Management** — Create, list, retrieve, and update projects.
- **Task Management** — Create, list, retrieve, and update tasks.
- **PostgreSQL Database** — Persistent relational data storage.
- **Role-Based Access Control (RBAC)** — Role-based permissions, according to the configured application rules.
- **RESTful API Design** — Structured endpoints with JSON request and response bodies.
- **API Testing** — Manual endpoint testing using Postman.
- **Docker Support** — Containerized development setup, if configured.

## Tech Stack

- **Language:** Python
- **Backend Framework:** Django
- **API Framework:** Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT
- **API Testing:** Postman
- **Containerization:** Docker and Docker Compose

## Project Structure

```text
enterprise-task-api/
├── accounts/
├── common/
├── projects/
├── tasks/
├── manage.py
├── requirements.txt
├── docker-compose.yml
└── README.md
```

*The structure may vary depending on your actual project files.*

## Getting Started

### Prerequisites

Make sure you have installed:

- Python
- PostgreSQL
- Git
- Postman (for API testing)

Docker is optional if you use the containerized setup.

### 1. Clone the Repository

```bash
git clone https://github.com/MKdir75/enterprise-task-api.git
cd enterprise-task-api
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Configure your Django secret key and PostgreSQL database credentials according to the settings used in your project.

Example configuration:

```env
DEBUG=True
SECRET_KEY=your-development-secret-key
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

These are example variable names. Use the exact names expected by your Django settings. Never commit real credentials or production secrets to GitHub.

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

The local development server will normally be available at:

```text
http://127.0.0.1:8000/
```

## API Endpoints

The following endpoints have been manually tested during development.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/projects/` | Create a project |
| GET | `/api/projects/` | List projects |
| GET | `/api/projects/<id>/` | Retrieve project details |
| PATCH | `/api/projects/<id>/` | Update project fields |
| GET | `/api/tasks/` | List tasks |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/<id>/` | Retrieve task details |
| PATCH | `/api/tasks/<id>/` | Update task fields |

Replace `<id>` with the relevant resource ID.

## Authentication

Protected endpoints require a valid access token if JWT authentication is enabled for that endpoint.

1. Register or create a user using the configured authentication flow.
2. Log in to obtain an access token.
3. Open Postman and select **Authorization**.
4. Choose **Bearer Token**.
5. Enter the access token.
6. Send the API request.

Never share access tokens, refresh tokens, passwords, or secret keys publicly.

## Example Requests

### Create a Project

**POST** `/api/projects/`

```json
{
  "name": "Enterprise API Project",
  "description": "Project and task management backend",
  "status": "PLANNING"
}
```

### Create a Task

**POST** `/api/tasks/`

```json
{
  "title": "Implement JWT Authentication",
  "description": "Implement login and token refresh functionality",
  "project": 1,
  "status": "TODO",
  "priority": "HIGH"
}
```

Send these requests with the required authorization header. The accepted fields and choice values depend on the serializers and models configured in the application.

## Testing

The API has been manually tested using Postman for the following workflows:

- Project creation and retrieval
- Project listing and partial updates
- Task creation and retrieval
- Task listing and partial updates
- JSON request and response handling

Additional tests should verify invalid tokens, missing authentication, input validation, and access restrictions between different users.

## Security Considerations

Before production deployment:

- Disable Django debug mode.
- Use a strong, private secret key.
- Store database credentials in environment variables.
- Verify authentication and object-level permissions.
- Restrict allowed hosts and configure CORS appropriately.
- Enable HTTPS.
- Validate incoming request data.
- Avoid
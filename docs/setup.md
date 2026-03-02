# Setup and Installation

FreeQueues is designed to be easily deployed using Docker. This guide will walk you through setting up a development and production environment.

## Prerequisites

Ensure you have the following installed on your system:
-   **Docker Engine** (24.0.0 or higher)
-   **Docker Compose V2**
-   **Git**

## Quick Start (Docker)

To get the entire system up and running quickly:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-repo/freequeues.git
    cd freequeues
    ```

2.  **Environment Configuration:**
    Create a `.env` file in the root directory and configure the following variables (you can use `.env.example` as a template if it exists):
    ```env
    # Database
    POSTGRES_DB=freequeue
    POSTGRES_USER=freequeue
    POSTGRES_PASSWORD=your_secure_password

    # Redis
    REDIS_PASSWORD=your_redis_password

    # Django
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1,backend

    # SMS Gateway (Kannel)
    KANNEL_PASSWORD=your_kannel_password

    # Ports
    APP_PORT=80
    GRAFANA_PORT=3000
    ```

3.  **Build and Start:**
    ```bash
    docker compose up --build -d
    ```

4.  **Database Initialization:**
    The system will automatically run migrations on startup. To create a superuser for the admin dashboard:
    ```bash
    docker compose exec backend python manage.py createsuperuser
    ```

5.  **Access the Application:**
    -   **Frontend:** `http://localhost` (or your configured `APP_PORT`)
    -   **Backend Admin:** `http://localhost/admin/`
    -   **API Documentation:** `http://localhost/api/v1/docs/` (Swagger)
    -   **Monitoring (Grafana):** `http://localhost:3000`

## Manual Backend Setup (Local Development)

If you prefer to run the backend without Docker (e.g., for faster debugging):

1.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3.  **Run Services:**
    You will still need Redis and PostgreSQL running locally or in containers.
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

4.  **Celery Worker:**
    ```bash
    celery -A config worker --loglevel=info
    ```

5.  **Celery Beat:**
    ```bash
    celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    ```

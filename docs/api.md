# API Documentation

FreeQueues exposes a comprehensive RESTful API for all platform interactions. The API is built using Django REST Framework and follows standard HTTP practices.

## Overview

-   **Base URL:** `/api/v1/`
-   **Authentication:** JWT (JSON Web Token) via the `Authorization` header (`Bearer <token>`).
-   **Response Format:** JSON.

## Interactive Documentation

The system includes built-in interactive documentation powered by **drf-spectacular**. These endpoints provide real-time information about available endpoints, request parameters, and response schemas.

-   **Swagger UI:** `/api/v1/docs/` - A user-friendly, interactive explorer for the API.
-   **Redoc:** `/api/v1/redoc/` - A more structured, documentation-focused view.
-   **Schema (YAML/JSON):** `/api/v1/schema/` - Downloadable OpenAPI 3.0 specification.

## Core Endpoints (Highlights)

### 1. Authentication (`/accounts/`)
-   `POST /accounts/users/`: Register a new user.
-   `POST /accounts/jwt/create/`: Obtain a JWT token.
-   `POST /accounts/jwt/refresh/`: Refresh an expired token.

### 2. Business Management (`/core/`)
-   `GET /core/branches/`: List all business branches.
-   `GET /core/branches/{id}/services/`: List services offered at a specific branch.
-   `POST /core/service-points/`: Create or update counters.

### 3. Queue Operations (`/core/`)
-   `POST /core/queue-entries/`: Join a queue.
-   `GET /core/queue-entries/me/`: View your current active queue status.
-   `PATCH /core/queue-entries/{id}/`: Update status (e.g., staff calling a customer).

### 4. Real-time Notifications (WebSockets)
-   **Endpoint:** `/ws/queue/branch_{branch_id}/`
-   Connect to this socket to receive real-time updates for a specific branch's queue.

## Error Handling

The API uses standard HTTP status codes:
-   `200 OK`: Success.
-   `201 Created`: Resource created successfully.
-   `400 Bad Request`: Validation error or invalid input.
-   `401 Unauthorized`: Missing or invalid authentication token.
-   `403 Forbidden`: Authenticated but lacking necessary permissions.
-   `404 Not Found`: Resource does not exist.
-   `500 Internal Server Error`: An unexpected error occurred on the server.

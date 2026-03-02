# System Architecture

FreeQueues is built on a modern, distributed architecture to ensure reliability, scalability, and real-time responsiveness. The system leverages a microservices-inspired approach with Docker for containerization and orchestration.

## High-Level Overview

The system is composed of several key layers:

### 1. Presentation Layer (Frontend)
-   **Web Application:** Built with React, providing a responsive interface for both business administrators and customers.
-   **Mobile Application:** Developed using React Native for on-the-go queue management and remote joining.

### 2. Application Layer (Backend)
-   **Framework:** Django with Django REST Framework (DRF) for robust API development.
-   **Real-time Engine:** Django Channels handles WebSocket connections for real-time queue updates and notifications.
-   **Task Queue:** Celery with Redis for asynchronous processing, such as sending SMS notifications and generating reports.
-   **AI Assistant:** Integrated LangChain-based assistant for intelligent customer interactions and automated support.

### 3. Data & Messaging Layer
-   **Primary Database:** PostgreSQL for structured, relational data (users, businesses, branches, queue entries).
-   **Cache & Broker:** Redis serves as both a high-speed cache and the message broker for Celery and Channels.
-   **SMS Gateway:** Kannel (Bearerbox & Smsbox) provides a reliable interface for SMPP-based SMS delivery.

### 4. Infrastructure & Monitoring
-   **Reverse Proxy:** Nginx handles SSL termination, static file serving, and request routing.
-   **Containerization:** Docker and Docker Compose for environment consistency across development and production.
-   **Observability:**
    -   **Prometheus:** Collects system and application metrics.
    -   **Grafana:** Provides visual dashboards for monitoring system health and queue performance.
    -   **Loki:** (Optional) Integrated log aggregation.

## System Components (Backend Apps)

-   **`accounts`:** Manages user profiles, authentication (JWT/Djoser), and permission levels (Admin, Staff, Customer).
-   **`core`:** The heartbeat of the system, containing business logic for branches, services, service points, and the queue engine.
-   **`assistant`:** AI-powered module for automated interactions and local knowledge retrieval.
-   **`stats`:** Aggregates data for business intelligence and operational reporting.
-   **`general_settings`:** Centralized configuration management for application-wide parameters.

## Data Flow (Real-time Queue Update)

1.  **Action:** A customer joins a queue via the Web/Mobile App.
2.  **API Call:** The frontend sends a POST request to the Backend.
3.  **Processing:** `core` app validates and creates a new QueueEntry in PostgreSQL.
4.  **Broadcast:** Django Channels triggers a WebSocket broadcast to all connected clients in that branch's group.
5.  **UI Update:** The frontend receives the WebSocket message and updates the queue list in real-time without a page refresh.
6.  **Background:** Celery sends an SMS notification to the customer confirming their position.

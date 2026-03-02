# FreeQueues

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-5.2+-green.svg)](https://www.djangoproject.com/)

FreeQueues is a professional **Queue Management System (QMS)** designed to streamline customer flow and reduce physical wait times. It provides businesses with tools to efficiently manage customer queues while offering customers the convenience of joining queues remotely and tracking their position in real-time.

## 🚀 Key Features

-   **Multi-Branch Support:** Manage multiple business locations from a central dashboard.
-   **Real-time Updates:** Powered by WebSockets (Django Channels) for live queue status.
-   **Remote Queue Joining:** Customers can join queues from anywhere via Web or Mobile apps.
-   **SMS Notifications:** Integrated Kannel SMS gateway for automated alerts and confirmations.
-   **AI Assistant:** Smart assistant powered by LangChain for intelligent customer support.
-   **Observability:** Built-in monitoring with Prometheus and Grafana.

## 📖 Documentation

For detailed information, please refer to the following guides:

-   [**Introduction**](docs/introduction.md): Project overview and core principles.
-   [**System Architecture**](docs/architecture.md): Deep dive into the tech stack and system design.
-   [**Features**](docs/features.md): Comprehensive breakdown of business and customer features.
-   [**Setup & Installation**](docs/setup.md): Guide to getting the system running locally or via Docker.
-   [**API Documentation**](docs/api.md): Overview of REST API endpoints and real-time sockets.
-   [**Deployment Guide**](docs/deployment.md): Production deployment best practices.
-   [**Contributing**](docs/contributing.md): Guidelines for developers wishing to contribute.

## 🛠 Tech Stack

-   **Backend:** Django, Django REST Framework, Django Channels (WebSockets)
-   **Frontend:** React, React Native
-   **Data:** PostgreSQL, Redis
-   **Tasks:** Celery
-   **Infrastructure:** Docker, Nginx, Prometheus, Grafana
-   **Messaging:** Kannel (SMS Gateway)

## 🚦 Quick Start

To start the entire system using Docker:

```bash
git clone https://github.com/your-repo/freequeues.git
cd freequeues
cp .env.example .env  # Configure your environment variables
docker compose up --build -d
```

The application will be available at `http://localhost`.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (if available).

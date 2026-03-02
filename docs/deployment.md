# Deployment Guide

This guide covers the deployment of FreeQueues for production environments.

## Deployment Strategy

FreeQueues is designed to be deployed using **Docker Compose** or **Kubernetes**. For most use cases, Docker Compose provides a robust and manageable solution.

### 1. Security Checklist
-   **SSL/TLS:** Always use HTTPS. Nginx should be configured with SSL certificates (e.g., Let's Encrypt).
-   **Secret Management:** Never commit `.env` files. Use a secure vault or environment variables provided by your host.
-   **Database Access:** Ensure PostgreSQL and Redis are not exposed to the public internet. Use internal Docker networks.
-   **Security Groups/Firewall:** Only open necessary ports (e.g., 80, 443).

### 2. Static and Media Files
In production, Django is configured to use **WhiteNoise** or a dedicated Nginx volume for serving static assets. Ensure `COLLECTSTATIC` is run during the build process.

### 3. Monitoring in Production
FreeQueues includes a production-ready monitoring stack:
-   **Prometheus:** Scrapes metrics from the `/api/v1/metrics/` endpoint (powered by `django-prometheus`).
-   **Grafana:** Provides pre-configured dashboards for visualizing system health and queue metrics.
-   **Kannel:** Monitor the SMS gateway status at `http://bearerbox:13000/status.txt`.

## Infrastructure Requirements (Minimum)
-   **CPU:** 2 Cores
-   **RAM:** 4GB
-   **Storage:** 20GB SSD
-   **OS:** Linux (Ubuntu 22.04 LTS recommended)

## Deployment Command (Production)
```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Run in detached mode
docker compose -f docker-compose.prod.yml up -d
```

## Scaling
-   **Backend:** Can be scaled horizontally by running multiple `backend` containers behind a load balancer (Nginx).
-   **Workers:** Celery workers can be scaled independently based on the volume of background tasks (e.g., high SMS traffic).
-   **Database:** For large-scale deployments, consider a managed PostgreSQL service (e.g., AWS RDS, DigitalOcean Managed DB).

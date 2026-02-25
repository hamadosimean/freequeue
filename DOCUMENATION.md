# FreeQueues

## Overview

FreeQueues is a modern Queue Management System (QMS) designed to streamline customer flow and reduce wait times. It provides businesses with tools to efficiently manage customer queues while offering customers the convenience of joining queues remotely and tracking their position in real-time.

## Core Principles

### For Businesses

- Register and manage multiple business branches
- Create and configure service points (counters/gichets)
- Enable remote queue joining for customers
- Monitor queue metrics and customer flow in real-time

### For Customers

- Create an account and browse available businesses
- Join queues remotely from anywhere
- View real-time queue length and estimated wait time
- Leave queues at any time with automatic notifications

## Key Features

### Business Management

- Multi-branch support with centralized management
- Service point configuration and customization
- Real-time queue monitoring and analytics
- Customer notifications via SMS

### Customer Experience

- Remote queue joining
- Real-time queue status updates
- Estimated wait time calculations
- Queue departure notifications

## Technology Stack

### Frontend & Mobile

- **Web**: React
- **Mobile**: React Native

### Backend

- **Framework**: Django, Django REST Framework
- **Real-time Communication**: Django Channels (WebSocket)
- **Authentication**: JWT, Djoser

### Data & Caching

- **Database**: PostgreSQL
- **Cache**: Redis

### Infrastructure

- **Background Tasks**: Celery with Redis
- **Monitoring**: Prometheus, Grafana, Loki
- **Deployment**: Docker, Kubernetes
- **SMS Gateway**: Kannel, SMPP

## Application Structure

- **Core**: Contains the core business logic and queue management functionality
- **Accounts**: Handles user management, authentication, and authorization
- **Stats**: Provides statistical analysis and reporting features

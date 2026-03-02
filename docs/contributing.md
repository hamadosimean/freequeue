# Contributing Guidelines

We welcome contributions to FreeQueues! To ensure a smooth process, please follow these guidelines.

## Getting Started

1.  **Fork the repository.**
2.  **Create a new branch:** `git checkout -b feature/your-feature-name` or `bugfix/your-fix-name`.
3.  **Set up your environment:** Follow the [Setup Guide](setup.md).
4.  **Write tests:** Ensure any new code is covered by unit and integration tests.

## Coding Standards

### Backend (Django)
-   Follow **PEP 8** for Python code.
-   Use descriptive variable and function names.
-   Ensure all API endpoints are documented with type hints and docstrings.
-   Run `flake8` or `ruff` for linting before submitting a PR.

### Frontend (React)
-   Follow the existing component structure and naming conventions.
-   Use functional components with hooks.
-   Ensure responsive design and accessibility.

## Commits

-   Use clear, concise commit messages.
-   Reference any related issue numbers (e.g., "Fixes #123").
-   Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## Pull Request Process

1.  **Update documentation:** If you add a new feature or change existing behavior, update the relevant files in `docs/`.
2.  **Verify build:** Ensure all tests pass and the Docker build is successful.
3.  **Submit PR:** Provide a detailed description of your changes and why they are needed.

## Community & Support

If you have questions or need help, please open an issue or join our community discussion board.

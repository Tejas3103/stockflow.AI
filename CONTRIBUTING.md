# Contributing to stockflow.AI

We welcome contributions to `stockflow.AI`! Whether you're fixing bugs, adding new features, or improving documentation, your help is greatly appreciated. Please take a moment to review this document to ensure a smooth contribution process.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Request Guidelines](#pull-request-guidelines)
- [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Local Setup](#local-setup)
  - [Running Tests](#running-tests)
- [Styleguides](#styleguides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Styleguide](#python-styleguide)
  - [TypeScript/React Styleguide](#typescriptreact-styleguide)

## Code of Conduct

We adhere to a [Code of Conduct](CODE_OF_CONDUCT.md) that all contributors are expected to follow. Please read it before contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please open a new [Bug Report issue](https://github.com/Tejas3103/stockflow.AI/issues/new?template=bug_report.md). Include:

- A clear and concise description of the bug.
- Steps to reproduce the behavior.
- Expected behavior.
- Screenshots if applicable.
- Your operating system, browser, and version.

### Suggesting Enhancements

If you have an idea for a new feature or an improvement, please open a new [Feature Request issue](https://github.com/Tejas3103/stockflow.AI/issues/new?template=feature_request.md). Include:

- A clear and concise description of the enhancement.
- Why this feature would be useful.
- Any alternative solutions or features you've considered.

### Your First Code Contribution

If you're new to contributing, start by looking for issues labeled `good first issue` or `help wanted`.

1.  **Fork the repository** to your GitHub account.
2.  **Clone your forked repository** to your local machine:
    ```bash
    git clone https://github.com/YOUR_USERNAME/stockflow.AI.git
    cd stockflow.AI
    ```
3.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout main
    git pull origin main
    git checkout -b feature/your-feature-name # or bugfix/your-bugfix-name
    ```
4.  **Make your changes.**
5.  **Test your changes** to ensure they work as expected and don't introduce new bugs.
6.  **Commit your changes** using a descriptive commit message (see [Git Commit Messages](#git-commit-messages)).
7.  **Push your branch** to your forked repository:
    ```bash
    git push origin feature/your-feature-name
    ```
8.  **Open a Pull Request** to the `main` branch of the original `stockflow.AI` repository (see [Pull Request Guidelines](#pull-request-guidelines)).

### Pull Request Guidelines

When submitting a pull request, please ensure:

- It targets the `main` branch.
- It addresses a single, well-defined problem or feature.
- All tests pass.
- Your code adheres to our styleguides.
- The PR description is clear and concise.
- If applicable, link to the related issue (e.g., `Closes #123`).
- You have read and agreed to our [Code of Conduct](CODE_OF_CONDUCT.md).

## Development Setup

### Prerequisites

- Node.js (for frontend)
- npm (Node Package Manager)
- Python 3.10+ (for backend)
- pip (Python Package Installer)

### Local Setup

1.  **Backend Setup:**
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```
2.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

### Running Tests

To run backend tests:

```bash
p pytest backend/test_api.py
```

*(Note: Frontend tests are not yet set up, but will be added in the future.)*

## Styleguides

### Git Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This helps us write clear commit messages and automate versioning.

Examples:

- `feat: Add new stock analysis agent`
- `fix: Correct API error handling`
- `docs: Update README with setup instructions`
- `refactor: Improve code readability in main.py`

### Python Styleguide

We generally follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code. We recommend using a linter like `flake8` or `black`.

### TypeScript/React Styleguide

For TypeScript and React, we adhere to standard practices and recommend using `ESLint` and `Prettier` for consistent formatting and code quality. 
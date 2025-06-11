# Contributing to StockFlow.AI 🤝

Thank you for your interest in contributing to StockFlow.AI! This document provides guidelines for contributing to this project.

## 🚀 Quick Start

1. **Fork the repository**
2. **Create a feature branch** from `develop`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a Pull Request**

## 📋 Branch Strategy

- `main` - Production-ready code (protected)
- `develop` - Integration branch for features
- `feature/*` - Feature development branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Critical production fixes

## 🔒 Branch Protection Rules

- **No direct pushes to `main`** - All changes must go through Pull Requests
- **Required reviews** - At least one maintainer must approve
- **Status checks** - All tests must pass before merging
- **Up-to-date branches** - Must be up-to-date with target branch

## 🛠️ Development Setup

### Prerequisites
- Node.js (v16+)
- Python 3.8+
- Git

### Local Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/stockflow.AI.git
cd stockflow.AI

# Set up backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up frontend
cd frontend
npm install
```

### Running the Application
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

## 📝 Code Style

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Add docstrings for functions
- Maximum line length: 88 characters

### TypeScript/React (Frontend)
- Use TypeScript strict mode
- Follow ESLint rules
- Use functional components with hooks
- Prefer named exports

## 🧪 Testing

### Backend Tests
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=backend
```

### Frontend Tests
```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## 📤 Submitting Changes

1. **Create a feature branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Target the `develop` branch
   - Use the PR template
   - Describe your changes clearly
   - Link any related issues

## 🏷️ Commit Message Convention

Use conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

## 🔍 Pull Request Guidelines

### PR Title Format
```
type(scope): description

Examples:
feat(ui): add dark mode toggle
fix(api): resolve CORS issue
docs(readme): update installation guide
```

### PR Description Template
```markdown
## 🎯 Description
Brief description of changes

## 📋 Changes Made
- [ ] Change 1
- [ ] Change 2
- [ ] Change 3

## 🧪 Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## 📸 Screenshots (if applicable)
Add screenshots for UI changes

## 🔗 Related Issues
Closes #123
```

## 🎨 UI/UX Guidelines

### Design Principles
- **Consistency** - Follow existing design patterns
- **Accessibility** - Ensure WCAG 2.1 AA compliance
- **Responsive** - Work on all screen sizes
- **Performance** - Optimize for speed

### Color Palette
- Primary: `#007bff` (Blue)
- Secondary: `#6c757d` (Gray)
- Success: `#28a745` (Green)
- Warning: `#ffc107` (Yellow)
- Danger: `#dc3545` (Red)

## 🐛 Bug Reports

When reporting bugs, please include:
- **Environment** - OS, browser, versions
- **Steps to reproduce** - Clear, numbered steps
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Screenshots** - Visual evidence if applicable

## 💡 Feature Requests

When requesting features, please include:
- **Use case** - Why is this feature needed?
- **Proposed solution** - How should it work?
- **Alternatives considered** - What other approaches were considered?
- **Additional context** - Any other relevant information

## 🤝 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's coding standards

## 📞 Getting Help

- **Issues** - For bugs and feature requests
- **Discussions** - For questions and general discussion
- **Pull Requests** - For code contributions

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

---

**Thank you for contributing to StockFlow.AI! 🚀** 
# Contributing to GradStat

Thank you for your interest in contributing to GradStat! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, versions)

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear use case
   - Expected behavior
   - Potential implementation approach
   - Impact on existing functionality

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow code style guidelines
   - Add tests for new functionality
   - Update documentation
4. **Commit your changes**: `git commit -m "Add feature: description"`
5. **Push to your fork**: `git push origin feature/your-feature-name`
6. **Create a Pull Request**

## Development Setup

### Prerequisites

- Node.js 18+
- Python 3.10+
- Docker and Docker Compose

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/gradstat.git
cd gradstat

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
npm install

# Install worker dependencies
cd ../worker
pip install -r requirements.txt
```

### Running Tests

```bash
# Backend tests
cd backend
npm test

# Worker tests
cd worker
pytest

# E2E tests
cd e2e
npm install
npx playwright install
npm test
```

## Code Style Guidelines

### TypeScript/JavaScript

- Use TypeScript for new frontend code
- Follow ESLint and Prettier configurations
- Use functional components and hooks in React
- Prefer `const` over `let`
- Use meaningful variable names
- Add JSDoc comments for functions

### Python

- Follow PEP 8 style guide
- Use type hints
- Add docstrings for functions and classes
- Use `black` for formatting
- Use `flake8` for linting

### Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Examples:
```
Add group comparison analysis
Fix regression plot rendering issue
Update documentation for deployment
```

## Project Structure

```
gradstat/
├── frontend/          # React TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   ├── types.ts
│   │   └── App.tsx
│   └── package.json
├── backend/           # Node.js Express backend
│   ├── server.js
│   └── package.json
├── worker/            # Python FastAPI analysis worker
│   ├── analyze.py
│   ├── analysis_functions.py
│   └── requirements.txt
├── e2e/              # End-to-end tests
├── k8s/              # Kubernetes manifests
└── docker-compose.yml
```

## Adding New Analysis Types

To add a new statistical analysis:

1. **Add analysis function** in `worker/analysis_functions.py`:
```python
def your_analysis(df: pd.DataFrame, opts: Dict) -> Dict:
    # Implement analysis logic
    return {
        "analysis_type": "your-analysis",
        "summary": "...",
        "test_results": {...},
        "plots": [...],
        "interpretation": "...",
        "code_snippet": "..."
    }
```

2. **Update frontend** in `frontend/src/components/AnalysisSelector.tsx`:
   - Add option to select dropdown
   - Add configuration fields if needed

3. **Add tests** in `worker/test_analyze.py`

4. **Update documentation**

## Testing Guidelines

- Write tests for all new features
- Maintain or improve code coverage
- Test edge cases and error conditions
- Use descriptive test names

## Documentation

- Update README.md for user-facing changes
- Update DEPLOYMENT.md for infrastructure changes
- Add inline comments for complex logic
- Update API documentation (openapi.yaml)

## Review Process

1. All PRs require at least one review
2. CI checks must pass
3. Code coverage should not decrease
4. Documentation must be updated

## Questions?

- Open an issue for questions
- Join our community discussions
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

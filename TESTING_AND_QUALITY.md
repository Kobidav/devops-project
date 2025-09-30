# Code Quality and Testing Guide

This project includes comprehensive code quality checks, security scanning, and automated testing as part of the CI/CD pipeline.

## 🧪 Testing Framework

### Unit Tests
- **Framework**: pytest with coverage reporting
- **Location**: `tests/` directory
- **Configuration**: `pyproject.toml` (pytest.ini_options section)

### Test Coverage
- **Minimum Coverage**: 80%
- **Reports**: XML and HTML formats
- **Integration**: Codecov for coverage tracking

### Running Tests Locally
```bash
# Install development dependencies
poetry install --with dev

# Run all tests with coverage
pytest --cov=. --cov-report=term-missing --cov-report=html

# Run specific test file
pytest tests/test_backend_app.py -v

# Run tests with specific markers
pytest -m "not slow" -v
```

## 🔍 Code Quality Tools

### 1. Black - Code Formatter
- **Purpose**: Automatic Python code formatting
- **Configuration**: `pyproject.toml` (tool.black section)
- **Usage**: `black .`

### 2. isort - Import Sorter  
- **Purpose**: Sorts and organizes Python imports
- **Configuration**: `pyproject.toml` (tool.isort section)
- **Usage**: `isort .`

### 3. flake8 - Linter
- **Purpose**: Style guide enforcement and error detection
- **Configuration**: `.flake8` file
- **Usage**: `flake8 .`

### 4. mypy - Static Type Checker
- **Purpose**: Static type checking for Python
- **Configuration**: `pyproject.toml` (tool.mypy section)
- **Usage**: `mypy . --ignore-missing-imports`

### 5. pylint - Code Analysis
- **Purpose**: Comprehensive code analysis and quality metrics
- **Configuration**: `pyproject.toml` (tool.pylint section)
- **Usage**: `pylint *.py`

## 🔐 Security Scanning

### 1. Bandit - Security Linter
- **Purpose**: Identifies common security issues in Python code
- **Configuration**: `.bandit` file and `pyproject.toml`
- **Usage**: `bandit -r . -ll`

### 2. Safety - Dependency Scanner
- **Purpose**: Checks for known security vulnerabilities in dependencies
- **Usage**: `safety check`

### 3. Trivy - Container Security Scanner
- **Purpose**: Scans Docker images for vulnerabilities
- **Integration**: Runs automatically in CI/CD pipeline
- **Formats**: SARIF (for GitHub Security tab) and table format

## 🚀 CI/CD Pipeline Jobs

### 1. Code Quality Job
- ✅ Black formatting check
- ✅ isort import sorting check  
- ✅ flake8 linting
- ✅ pylint code analysis
- ✅ mypy type checking
- ✅ bandit security scanning
- ✅ safety dependency scanning

### 2. Test Job
- ✅ Unit tests with pytest
- ✅ Coverage reporting (80% minimum)
- ✅ PostgreSQL integration testing
- ✅ Codecov integration
- ✅ Test result artifacts

### 3. Container Security Job
- ✅ Trivy vulnerability scanning
- ✅ SARIF report upload to GitHub Security
- ✅ Critical/High severity blocking
- ✅ Multi-format reporting

### 4. Build and Push Job
- ✅ Multi-platform Docker builds (AMD64/ARM64)
- ✅ Docker Hub publishing
- ✅ Build provenance attestation
- ✅ Semantic versioning

### 5. Security Summary Job
- ✅ Aggregated security report
- ✅ GitHub step summary
- ✅ Artifact management

## 🛠️ Local Development Setup

### Install Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

### Development Dependencies
```bash
# Install all dependencies including dev tools
poetry install --with dev

# Or using pip
pip install -e ".[dev]"
```

### IDE Configuration

#### VS Code
Recommended extensions:
- Python
- Pylance
- Black Formatter
- isort
- Flake8
- mypy
- Bandit

#### Settings (`.vscode/settings.json`):
```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.banditEnabled": true,
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true
}
```

## 📊 Quality Metrics

### Code Coverage
- **Target**: 80% minimum
- **Current**: Tracked in CI/CD pipeline
- **Reports**: Available in artifacts

### Security Scanning
- **Bandit**: Security issues in code
- **Safety**: Vulnerable dependencies  
- **Trivy**: Container vulnerabilities

### Code Quality Scores
- **flake8**: Style and error checking
- **pylint**: Code quality rating
- **mypy**: Type coverage

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Main project configuration |
| `.flake8` | flake8 linting rules |
| `.bandit` | Security scanning config |
| `.pre-commit-config.yaml` | Pre-commit hooks |
| `.yamllint.yml` | YAML linting rules |

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors in Tests**
   ```bash
   # Add project root to Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Coverage Too Low**
   ```bash
   # Run with coverage details
   pytest --cov=. --cov-report=term-missing
   ```

3. **Type Checking Errors**
   ```bash
   # Install type stubs
   pip install types-requests types-psycopg2
   ```

4. **Pre-commit Hook Failures**
   ```bash
   # Update hooks
   pre-commit autoupdate
   
   # Skip hooks temporarily
   git commit --no-verify
   ```

## 📈 Monitoring and Reporting

### GitHub Integration
- **Security Tab**: SARIF reports from Trivy
- **Actions Tab**: CI/CD pipeline results
- **Pull Requests**: Automated checks and reports

### External Services
- **Codecov**: Coverage tracking and reporting
- **Docker Hub**: Image vulnerability scanning

### Artifacts
- Security scan reports (JSON format)
- Test coverage reports (XML/HTML)
- Build logs and summaries
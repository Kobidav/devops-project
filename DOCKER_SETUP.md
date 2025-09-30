# Docker Hub GitHub Action Setup

This repository includes a comprehensive CI/CD pipeline that automatically builds, tests, scans, and pushes Docker images to Docker Hub with extensive quality and security checks.

## Prerequisites

Before the GitHub Action can work, you need to set up the following secrets in your GitHub repository:

### 1. Create Docker Hub Access Token

1. Go to [Docker Hub](https://hub.docker.com/)
2. Sign in to your account
3. Go to **Account Settings** → **Security**
4. Click **New Access Token**
5. Give it a descriptive name (e.g., "GitHub Actions")
6. Set permissions to **Read, Write, Delete**
7. Copy the generated token (you won't see it again!)

### 2. Add GitHub Repository Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add:

   - **Name**: `DOCKERHUB_USERNAME`
   - **Value**: Your Docker Hub username

   - **Name**: `DOCKERHUB_TOKEN`
   - **Value**: The access token you created in step 1

## Enhanced CI/CD Pipeline

The GitHub Action now includes comprehensive quality and security checks:

### 🔍 **Code Quality Job**
- **Black** code formatting validation
- **isort** import sorting verification
- **flake8** linting and style checks
- **pylint** comprehensive code analysis
- **mypy** static type checking
- **bandit** security vulnerability scanning
- **safety** dependency vulnerability checking

### 🧪 **Testing Job**
- **pytest** unit tests with 80% coverage requirement
- **PostgreSQL** integration testing
- **Codecov** coverage reporting
- Test artifacts and detailed reports

### 🔐 **Container Security Job**
- **Trivy** vulnerability scanning
- SARIF security reports uploaded to GitHub Security tab
- Critical/High severity vulnerability blocking
- Multi-format security reporting

### 🚀 **Build and Push Job**
- Multi-platform builds (AMD64 + ARM64)
- Smart caching for faster builds
- Semantic version tagging
- Build provenance attestation

### 📊 **Security Summary Job**
- Consolidated security reporting
- GitHub step summaries
- Artifact management

## How the Enhanced Workflow Works

The GitHub Action will:

1. **Trigger on**:
   - Push to `main` or `develop` branches
   - Creation of version tags (e.g., `v1.0.0`)
   - Pull requests to `main` (build and test only, no push)

2. **Quality Gates** (All must pass):
   - ✅ Code formatting (Black)
   - ✅ Import sorting (isort) 
   - ✅ Linting (flake8)
   - ✅ Type checking (mypy)
   - ✅ Security scanning (bandit)
   - ✅ Dependency scanning (safety)
   - ✅ Unit tests (80% coverage)
   - ✅ Container security (Trivy)

3. **Build Process** (Only after all checks pass):
   - Multi-platform Docker builds
   - Security attestation
   - Push to Docker Hub with semantic tags

## Pipeline Status and Reports

### GitHub Integration
- **Actions Tab**: Real-time pipeline status
- **Security Tab**: Automated SARIF vulnerability reports
- **Pull Requests**: Automatic quality checks and blocking
- **Step Summaries**: Consolidated security and quality reports

### Artifacts Generated
- Security scan reports (bandit, safety, trivy)
- Test coverage reports (XML and HTML)
- Code quality metrics

## Image Tags

After successful builds, your images will be available at:
```
docker.io/YOUR_DOCKERHUB_USERNAME/devops-project:latest
```

**Tagging Strategy**:
- `latest` - for pushes to main branch
- `main`, `develop` - for pushes to respective branches
- `v1.0.0`, `v1.0`, `v1` - for version tags
- `pr-123` - for pull requests (build only)

## Local Development

### Setup Development Environment
```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install all dependencies including development tools
poetry install --with dev

# Setup pre-commit hooks (optional but recommended)
poetry run pre-commit install
```

### Run Quality Checks Locally
```bash
# Format code
poetry run black .
poetry run isort .

# Run linting
poetry run flake8 .
poetry run pylint *.py

# Type checking
poetry run mypy . --ignore-missing-imports

# Security scanning
poetry run bandit -r . -ll
poetry run safety check

# Run tests
poetry run pytest --cov=. --cov-report=term-missing
```

### Test Docker Image Locally
```bash
# Build the image
docker build -t devops-project:local .

# Run the image (example with backend)
docker run -e exe="backend_app.py" -p 8080:8080 devops-project:local

# Run the image (example with frontend)
docker run -e exe="frontend_app.py" -p 8080:8080 devops-project:local
```

## Security Features

- **Multi-layered Security Scanning**:
  - Source code security (bandit)
  - Dependency vulnerabilities (safety)
  - Container vulnerabilities (Trivy)
- **Access Control**: Docker Hub tokens instead of passwords
- **Build Security**: Provenance attestation and SLSA compliance
- **Multi-platform Support**: AMD64 and ARM64 architectures
- **Dependency Pinning**: Lock files for reproducible builds

## Quality Assurance

- **Code Formatting**: Consistent style with Black
- **Import Management**: Organized imports with isort
- **Code Quality**: Multi-tool linting (flake8, pylint)
- **Type Safety**: Static type checking with mypy
- **Test Coverage**: 80% minimum coverage requirement
- **Integration Testing**: PostgreSQL database testing

## Troubleshooting

### Pipeline Failures

1. **Code Quality Issues**:
   ```bash
   # Fix formatting issues
   poetry run black .
   poetry run isort .
   ```

2. **Test Failures**:
   ```bash
   # Run tests locally with verbose output
   poetry run pytest -v --tb=short
   ```

3. **Security Vulnerabilities**:
   ```bash
   # Check specific security issues
   poetry run bandit -r . -f json
   poetry run safety check --json
   ```

4. **Coverage Too Low**:
   ```bash
   # Generate coverage report
   poetry run pytest --cov=. --cov-report=html
   # Open htmlcov/index.html to see detailed coverage
   ```

### Docker Issues

1. **Build Failures**:
   - Check Dockerfile syntax
   - Verify all COPY paths exist
   - Test build locally first

2. **Security Scan Failures**:
   - Review Trivy reports in GitHub Security tab
   - Update base image or dependencies
   - Consider using distroless images

For detailed information about testing and quality tools, see [TESTING_AND_QUALITY.md](TESTING_AND_QUALITY.md).
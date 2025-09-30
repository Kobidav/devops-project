# Docker Hub GitHub Action Setup

This repository includes a GitHub Action that automatically builds and pushes Docker images to Docker Hub.

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

## How the Workflow Works

The GitHub Action will:

1. **Trigger on**:
   - Push to `main` or `develop` branches
   - Creation of version tags (e.g., `v1.0.0`)
   - Pull requests to `main` (build only, no push)

2. **Build Process**:
   - Checks out the code
   - Sets up Docker Buildx for multi-platform builds
   - Logs into Docker Hub (only for pushes)
   - Extracts metadata for tagging
   - Builds the Docker image for `linux/amd64` and `linux/arm64`
   - Pushes to Docker Hub (except for PRs)
   - Generates build attestation for security

3. **Image Tags**:
   - `latest` - for pushes to main branch
   - `main`, `develop` - for pushes to respective branches
   - `v1.0.0`, `v1.0`, `v1` - for version tags
   - `pr-123` - for pull requests

## Docker Image Location

After successful builds, your images will be available at:
```
docker.io/YOUR_DOCKERHUB_USERNAME/devops-project:latest
```

## Local Testing

To test the Docker image locally:

```bash
# Build the image
docker build -t devops-project:local .

# Run the image (example with backend)
docker run -e exe="backend_app.py" -p 8080:8080 devops-project:local

# Run the image (example with frontend)
docker run -e exe="frontend_app.py" -p 8080:8080 devops-project:local
```

## Security Features

- Uses Docker Hub access tokens instead of passwords
- Builds are cached using GitHub Actions cache
- Multi-platform builds (AMD64 and ARM64)
- Build provenance attestation for supply chain security
- Only pushes on main branch and tags (not on PRs)
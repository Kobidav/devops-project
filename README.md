# devops-project

A simple Python-based application designed to help users learn and experiment with DevOps tools and practices. This project demonstrates containerization with Docker, running PostgreSQL as a service, and environment-based configuration for development workflows.

## Running with Docker

```bash
export POSTGRES_PASSWORD="my_postgress_password"
docker run -d --name postgres-container \
    -e TZ=UTC \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -p 30432:5432 \
    ubuntu/postgres

export DB_HOST=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres-container)

docker build . -t base
docker run \
    -e exe=frontend_app.py \
    -e DB_NAME=postgres \
    -e DB_USER=postgres \
    -e DB_HOST=$DB_HOST \
    -e DB_PORT=5432 \
    -e DB_PASSWORD=$POSTGRES_PASSWORD \
    base
docker run \
    -e exe=backend_app.py \
    -e DB_NAME=postgres \
    -e DB_USER=postgres \
    -e DB_HOST=$DB_HOST \
    -e DB_PORT=5432 \
    -e DB_PASSWORD=$POSTGRES_PASSWORD \
    base
```

## Optional: .env Template

```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

## Docker image

werta/devops-project

````markdown
## K8s manifests

The `k8s` folder contains Kubernetes manifests for deploying the devops-project application and its PostgreSQL database. These manifests include Deployment, Service, and ConfigMap resources to simplify running the project in a Kubernetes cluster.

### How to install

1. Ensure you have access to a Kubernetes cluster and `kubectl` is configured.
2. Apply the manifests in the `k8s` folder:

    ```bash
    kubectl apply -f k8s/
    ```

3. Check the status of your pods and services:

    ```bash
    kubectl get pods
    kubectl get services
    ```

Update the manifests as needed for your environment (e.g., database credentials, image tags).

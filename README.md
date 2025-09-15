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
```

## Optional: .env Template

```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

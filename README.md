# devops-project
simple python based app for learning devops tools


#### Run postgres in docker
```
docker run -d --name postgres-container -e TZ=UTC -p 30432:5432 -e POSTGRES_PASSWORD=YourPass ubuntu/postgres
docker container inspect postgres-container | grep IPAddress
```

#### .env template
```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```
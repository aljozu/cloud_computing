# Respuestas

## Respuesta de la **Actividad 1.1**

```bash
docker volume create boston-data
```

## Respuesta de la **Actividad 1.2**

```bash
docker run --name boston-db -d --rm -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=BOSTON -v boston-data:/var/lib/postgresql/data postgres:latest
```

## Respuesta de la **Actividad 1.3**

```bash
docker exec -it boston-db psql -U postgres -d BOSTON -c "CREATE TABLE IF NOT EXISTS product (
id SERIAL PRIMARY KEY,
name VARCHAR(255) UNIQUE,
description TEXT,
price NUMERIC,
stock INTEGER
);"
```


## Respuesta de la **Actividad 3.1**

```Dockerfile

```


## Respuesta de la **Actividad 3.2**

```bash
docker build -t app:v1.0 .
```


## Respuesta de la **Actividad 3.3**

```bash
# Comando incompleto
docker run -d --name boston-app -p 8080:8080 --rm app:v1.0
```

## Respuesta de la **Actividad 4.1**

```yml
docker tag app:v1.0 aljozu/mi-aplicacion:v1.0
```

## Respuesta de la **Actividad 5.1**

```bash
docker push aljozu/mi-aplicacion:v1.0
```
https://hub.docker.com/repository/docker/aljozu/mi-aplicacion/general
## Respuesta de la **Actividad 5.2**

```bash
docker-compose up -d
```
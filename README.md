<p align="center">
  <a href="https://www.linkedin.com/in/zakharb/flaskapi">
  <img src="img/logo.png" alt="logo" />
</p>

<p align="center">

  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=30&pause=1000&color=3E0576&center=true&width=500&lines=++Microservice+architecture;+with+Flask+and+Docker" alt="description" />
  </a>  
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.2-purple" height="20"/>
  <img src="https://img.shields.io/badge/python-3.11-purple" height="20"/>
</p>

## :purple_square: Getting Started

[FlaskAPI](https://github.com/zakharb/flaskapi) is fully separates API based on [Microservices](https://en.wikipedia.org/wiki/Microservices)   

For CRUD operations is used `Customer` model  

Each part is work like Microservice  
The Microservice runs in separate Docker container   

Microservice has its own Database  
Database can be switch from MongoDB to Postgres or other  

Also the API include 
- authentication mechanism using JWT tokens  
- pagination and filtering to limit the amount of data returned  
- use caching mechanism to improve performance for frequently accessed data  
- rate limiting to prevent abuse of the API


### Requirements

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

### Installing

Clone the project

```
git clone git@github.com:zakharb/flaskapi.git
cd flaskapi
```

Start docker-compose

```
docker-compose up -d
```

## :purple_square: Usage  

### Customers  

Login and get JWT token. Use it in protected requests
```sh
curl --location --request POST 'http://localhost:8080/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "admin",
    "password": "password"
}'
```

Add customer
```sh
curl --location --request POST 'http://localhost:8080/api/v1/customers' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3OTIzNDYyOCwianRpIjoiM2JlNzJjYjktY2QyYi00ZTcyLTg5M2YtOThkZTZhMDVlMTlhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNjc5MjM0NjI4LCJleHAiOjE2NzkyMzU1Mjh9.p_rJn8dHb3CIL4zPAgcG6qGsZxJOJZ8O6SL2GlJwGpY' \
--data-raw '{
    "name": "John Wick",
    "customer_class": "Enduser",
    "vat_percentage": 12,
    "status": "Active"
}'
```

Get customer by id
```sh
curl -X 'GET' 'http://localhost:8080/api/v1/customers/64170cf4236f4def3a87d600'
```

Get all customers
```sh
curl -X 'GET' 'http://localhost:8080/api/v1/customers/?page_size=3&page=2'
```

Update customer
```sh
curl --location --request PUT 'http://localhost:8080/api/v1/customers/6416c8af76181e5bd5641271' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer paste_token_here_eyJ...U' \
--data-raw '{
    "name": "John Doe",
    "customer_class": "Enduser",
    "vat_percentage": 11,
    "status": "Active"
}'
```

Delete customer
```sh
curl --location --request Delete 'http://localhost:8080/api/v1/customers/6416c8af76181e5bd5641271' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer paste_token_here_eyJ...U' \
```


## :purple_square: Configuration  
To solve problem with performance each Service run in container  
[Gunicorn]((https://www.gunicorn.org/)) work as WSGI server and connect to one piece with [Nginx](https://www.nginx.com/)  
Main configuration is `docker-compose.yml`  

- every service located in separate directory `name-service`  
- use `Dockerfile` to change docker installation settings  
- folder `app` contain FastAPI application  
- all services connected to one piece in `docker-compose.yml`  
- example of service + DB containers (change `--workers XX` to increase multiprocessing)  

### Examples  
`Customer` service
```
  customer_service:
    build: ./customer-service
    command: gunicorn app.main:app --bind 0.0.0.0:8000 --reload
    volumes:
      - ./customer-service/:/app/
    ports:
      - 8001:8000
    environment:
      - DATABASE_URI=mongodb://root:root@mongo:27017/
    depends_on:
       - customer_db
  
  customer_db:
    image: mongo
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root
    logging:
        driver: none
```

## :purple_square: Deployment

Edit `Dockerfile` for each Microservice and deploy container

## :purple_square: Versioning

Using [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/zakharb/flaskapi/tags). 

## :purple_square: Authors

* **Zakhar Bengart** - *Initial work* - [Ze](https://github.com/zakharb)

See also the list of [contributors](https://github.com/zakharb/flaskapi/contributors) who participated in this project.

## :purple_square: License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation - see the [LICENSE](LICENSE) file for details


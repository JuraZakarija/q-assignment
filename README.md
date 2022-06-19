# Q assignment

## Requirements 
Docker \
or \
Python 3.9+ on local machine 


## Setup
clone repo in desired folder \
create file .env in base directory and copy content from .env.tpl \
change SECRET_KEY

## With Docker - primary way
create file .env in base directory and copy content from .env.tpl \
> sudo docker-compose build \
> docker-compose up

## Without Docker - primary way

go to config/settings.py and uncomment sqlite database \
use command line to navigate to base folder \ 
create and activate virtual enviroment \
> python3 -m venv venv
> source venv/bin/activate

install dependencies
> pip install -r requirements.txt

migrate database
> python manage.py migrate

Import dummy data
> python manage.py import_dummy

Run tests
> python manage.py test

Run application
> python manage.py runserver

## Usage
go to http://localhost:8000/api/ for browserable api

admin url: http://localhost:8000/admin \

admin login:
>username: admin \
>password: admin

> for other users go to admin and copy username\
> password is testing321 for all users

swagger docs: http://localhost:8000/api/schema/swagger-ui/ \
redoc docs: http://localhost:8000/api/schema/redoc/

## Features
CRUD endpoints for products and product ratings \
Basic and JWT auth \
Listing pagination \
Dummy data generation \
Automatic documentation with Swagger and Redoc \
Unit tests \
Full text search when using Postgres \
Dockerized environment

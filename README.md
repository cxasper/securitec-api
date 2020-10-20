# Securitec-API

API that uses json for Securitec.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Docker
dockr-compose
```

### Installing

Clone repository
```
git clone git@github.com:cxasper/securitec-api.git
```

```
cd {{ project_name }}
```
Run project
```
docker-compose up -d --build
```

Run migration
```
docker-compose exec web python manage.py migrate
```

Create init user for project.
```
docker-compose exec web python manage.py createsuperuser
```

Run fixtures.
```
docker-compose exec web python manage.py loaddata apps/api/fixtures/countries.json
```

Run project
```
docker-compose exec web python manage.py runserver
```

## Running the tests

```
docker-compose exec web python manage.py test
```

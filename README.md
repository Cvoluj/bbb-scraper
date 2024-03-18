# bbb-scraper
This project uses [scrapy-boilerplate](https://github.com/groupbwt/scrapy-boilerplate) template

Scraping [bbb](https://www.bbb.org/)
## Features

- Python 3.11+
- [Poetry](https://github.com/python-poetry/poetry) for dependency management
- SQLAlchemy ORM with alembic migrations
- RabbitMQ integrated via [pika](https://github.com/pika/pika/)
- configuration via ENV variables and/or `.env` file
- single file for each class
- Docker-ready (see [here](#docker))
- PM2-ready
- supports single-IP/rotating proxy config out of the box (see [here](#proxy-middleware))

## Installation
Scrap bbb guide

1. Clone the repository.
2. `cp .env.example .env`
3. `docker compose up -d database python rmq`
3. `docker compose exec python bash`
4. `cd /var/app/python/src/`
5. `poetry shell`
Scrap sitemaps (url that we will scrap in RPC spider)
6. scrapy crawl sitemap
7. pm2 start pm2.config.js
8. scrapy export_csv

### Python Quickstart Guide
To create and run a new Scrapy project using this boilerplate, you need to:

1. Clone the repository.
2. `cp .env.example .env`
3. No docker:
   1. Have the following prerequisites: python 3.11+, poetry, mysqlclient libraries, etc
   2. `cd src/python/src`
   3. `poetry install`
   4. `poetry shell`
   5. `scrapy`
4. Docker:
   1. Have the following prerequisites: docker, docker-compose
   2. `docker compose up -d database python`
   3. `docker compose exec python bash`
   4. `cd /var/app/python/src/`
   5. `poetry shell`
   6. `scrapy`

### Docker

The project includes Dockerfiles and docker-compose configuration for running your spiders in containers.

Also, a configuration for default RabbitMQ server is included.

Dockerfiles are located inside the `docker` subdirectory, and the `docker-compose.yml` - at the root of the project.

Docker-compose takes configuration values from ENV. Environment can also be provided by creating a `.env` file at the root of the project (see `.env.example` as a sample).

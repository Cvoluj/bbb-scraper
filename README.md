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
3. `docker compose up -d rabbitmq`
3. `cd src/python/src`
4. `scrapy crawl sitemap`
5. `cd pm2/`
6. `pm2 start pm2.config.js`
7. `pm2 kill`
8. `cd ..`
9. `scrapy export_csv`

### Docker

The project includes Dockerfiles and docker-compose configuration for running your spiders in containers.

Also, a configuration for default RabbitMQ server is included.

Dockerfiles are located inside the `docker` subdirectory, and the `docker-compose.yml` - at the root of the project.

Docker-compose takes configuration values from ENV. Environment can also be provided by creating a `.env` file at the root of the project (see `.env.example` as a sample).

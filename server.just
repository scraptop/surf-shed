# Commands to run whilst logged in on the server.
# Usage: just -f server.just <command>

export COMPOSE_FILE := "docker-compose.production.yml"

# Default command to list all available commands.
default:
    @just --list

# up: Start production containers.
up:
    @docker compose up -d --remove-orphans

# down: Stop production containers.
down:
    @docker compose down

# logs: View production logs (optionally pass a service name, e.g: just -f server.just logs traefik).
logs *args:
    @docker compose logs -f {{args}}

# load: Load all production images from tar bundle.
load:
    docker load -i docker_prod_bundle.tar

# load-django: Load only the django image from tar.
load-django:
    docker load -i docker_django.tar

# load-traefik: Load only the traefik image from tar.
load-traefik:
    docker load -i docker_traefik.tar
    rm docker_traefik.tar

# check-file-size: Check disk usage.
check-file-size:
    du -h /usr/ 2>/dev/null | grep '[0-9\.]\+G'

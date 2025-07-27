export COMPOSE_FILE := "docker-compose.local.yml"

## Just does not yet manage signals for subprocesses reliably, which can lead to unexpected behavior.
## Exercise caution before expanding its usage in production environments.
## For more information, see https://github.com/casey/just/issues/2473 .


# Default command to list all available commands.
default:
    @just --list

# build: Build python image.
build:
    @echo "Building python image..."
    @docker compose build

# up: Start up containers.
up:
    @echo "Starting up containers..."
    @docker compose up -d --remove-orphans

# down: Stop containers.
down:
    @echo "Stopping containers..."
    @docker compose down

# prune: Remove containers and their volumes.
prune *args:
    @echo "Killing containers and removing volumes..."
    @docker compose down -v {{args}}

# logs: View container logs
logs *args:
    @docker compose logs -f {{args}}

# manage: Executes `manage.py` command.
manage +args:
    @docker compose run --rm django python ./manage.py {{args}}

# digitalocean server stuff
remote-root-cmd *args:
  ssh -i /home/sam/.ssh/surfshed/surfshed root@64.226.71.127:{{args}}

remote-root-login:
  ssh -i /home/sam/.ssh/surfshed/surfshed root@64.226.71.127

remote-surfshed-cmd *args:
  ssh -i /home/sam/.ssh/surfshed/surfshed surfshed@64.226.71.127:{{args}}

remote-surfshed-login:
  ssh -i /home/sam/.ssh/surfshed/surfshed surfshed@64.226.71.127

# do_surfshead is an alias for surfshed@ip-address
rsync-pwd:
  rsync -avh --exclude='db.sqlite3' --exclude='.git/' --exclude='.venv/' --include './.venvs/.*' ./ do_surfshed:/home/surfshed/cookiecutter-server

# build docker locally and save to tar
docker-save-all:
  docker save -o docker_prod_bundle.tar surf_shed_production_django surf_shed_production_traefik surf_shed_production_nginx surf_shed_production_postgres

docker-save-django:
  docker save -o docker_django surf_shed_production_django

docker-load:
  docker load -i docker_prod_bundle.tar

docker-load-django:
  docker load -i docker_django.tar

docker-clean:
  @echo "https://depot.dev/blog/docker-clear-cache"

check-file-size:
  du -h /usr/ 2>/dev/null | grep '[0-9\.]\+G'

check-stuff-inside-docker:
  docker run --rm -it --entrypoint /bin/ash surf_shed_production_traefik -c "cat /etc/traefik/traefik.yml"

django:
  docker compose -f docker-compose.local.yml run --rm django python manage.py compilemessages

# make linsurf user

# make superuser
migrate.py createsuperuser


# Change site to correct domainname
https://stackoverflow.com/questions/65733649/changing-default-django-site-name-and-domain-from-example-com-to-the-proper-ones
migrate.py shell
    >>> from django.contrib.sites.models import Site


    >>> my_site = Site.objects.get(name='example.com')
    >>> my_site.name = 'mysite.com'
    >>> my_site.domain = 'mysite.com'
    >>> my_site.save()


# stick your cert files to /certs directory



# build django container locally

    because there is not sufficient space on the machine
    also need to delete images and what not

    docker images rm <image>

# working with backups

    https://cookiecutter-django.readthedocs.io/en/latest/4-guides/docker-postgres-backups.html


# Dealing with very little resources on the server

There may be problem both with memory, ie cant build because 1gb of memory is not enough.
And or, you might have problem with disk space running out.
The following procedure should help with both problems (I found that only the django docker was problematic.
and could build the other images on the server.)

Build production docker on your local machine.

    export COMPOSE_FILE=docker-compose.production.yml
    docker compose build django
    # surf_shed_production_django is the image name
    docker save -o docker_django.tar surf_shed_production_django

Then scp or rsync the docker_django.tar file to the server.
On the server do:

    docker compose down
    docker images rm surf_shed_production_django
    docker load -i docker_django.tar

Now you can proceed with starting the containers:

    docker compose up --remove-orphans -d
    docker compose logs -f
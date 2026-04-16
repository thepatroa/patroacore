run:
	podman compose up

build:
	podman compose build

migrate:
	podman exec -it django_app python manage.py migrate

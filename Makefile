run:
	python manage.py runserver 0.0.0.0:8000

test:
	@echo 'Running tests'
	coverage run -m pytest
	coverage report
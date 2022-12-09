run:
	flask --app flaskr --debug run

init-db:
	flask --app flaskr init-db

create-env:
	python3 -m venv venv

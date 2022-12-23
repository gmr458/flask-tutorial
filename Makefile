dev:
	flask --app flaskr --debug run

create-env:
	python3 -m venv venv

install-dependencies:
	pip install -r requirements.txt

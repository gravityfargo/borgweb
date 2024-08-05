install:
	pip install -e .
	flask --app borgweb db init

clean:
	rm -rf dist src/*.egg-info src/instance
	find . -name '__pycache__' -exec rm -rf {} \; > /dev/null 2>&1
	

run:
	flask --app borgweb run

test:
	pytest 
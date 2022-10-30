run:
		docker-compose run --rm app
test:
		docker-compose run --rm test pytest
lint:
		docker-compose run --rm test pylint bot tests
format:
		docker-compose run --rm test autopep8 bot tests --in-place -r -a -a -a
build:
		docker-compose build

coverage:
		docker-compose run --rm test coverage run -m pytest
		docker-compose run --rm test coverage report -m

check: lint coverage

publish:
	docker build . -t kipelovets/lingvo_catalogue_bot:latest
	docker push kipelovets/lingvo_catalogue_bot:latest

deploy:
	kubectl apply -f k8s/deployment.yaml
	kubectl rollout restart deployment/lingvo-catalogue-bot
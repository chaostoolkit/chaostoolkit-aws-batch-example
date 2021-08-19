.PHONY: install
install:
	npm install
	poetry install

.PHONY: lint
lint:
	poetry run flake8 cdk/ experiment_image/
	poetry run isort --check-only --profile black cdk/ experiment_image/
	poetry run black --check --diff cdk/ experiment_image/

.PHONY: format
format:
	poetry run isort --profile black cdk/ experiment_image/
	poetry run black cdk/ experiment_image/

.PHONY: diff
diff:
	poetry run dotenv run npx cdk diff --app cdk/app.py || true

.PHONY: deploy
deploy:
	poetry run dotenv run npx cdk deploy --app cdk/app.py --require-approval never

.PHONY: destroy
destroy:
	poetry run dotenv run npx cdk destroy --app cdk/app.py --force

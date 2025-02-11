up:
	@gunicorn -b 0.0.0.0:8000 --workers 4 --threads 100 app.main:app

# migrate:
# 	@alembic upgrade head

# test:
# 	@alembic upgrade head
# 	@clear
# 	@pytest -s --durations=0 -v --cov=app

format:
	@isort app/
	@isort tests/
	@black app/
	@black tests/
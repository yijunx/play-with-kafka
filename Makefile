up:
	@gunicorn -b 0.0.0.0:8000 --workers 4 --threads 100 app.main:app

format:
	@isort app/
	@black app/
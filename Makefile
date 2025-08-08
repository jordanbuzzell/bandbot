.PHONY: install dev init-db clean

install:
	pip install -r backend/requirements.txt

init-db:
	python init_venues.py

dev:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

clean:
	rm -rf data/chroma/
	rm -rf __pycache__/
	rm -rf backend/__pycache__/
	rm -rf backend/app/__pycache__/

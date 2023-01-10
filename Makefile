include .env
export

test:
	pytest

run:
	python -m uvicorn crypto_tracker.main:app --reload
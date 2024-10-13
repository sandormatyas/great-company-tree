.PHONY: run-local
run-local:
	poetry run uvicorn src.main:app --reload


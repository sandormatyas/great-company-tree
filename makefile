.PHONY: run-local
run-local:
	DATABASE_URL="postgresql://postgres:postgres@localhost/company" poetry run uvicorn src.main:app --reload


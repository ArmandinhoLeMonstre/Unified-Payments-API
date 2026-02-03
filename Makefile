build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down -v

resetdb:
	rm -rf api/app/db/test.db
	touch api/app/db/test.db

dev:
	docker compose up --build -d
	cd frontend && npm run dev
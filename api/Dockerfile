FROM python:3.12

WORKDIR /code

COPY app/requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY ./app /code/app

# --reload is for restarting the server if changes are made in the code
# mount volumes have to be done in the docker compose
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--reload"] 

#use uvicorn in prod, fastapi in dev
# Do a dockerignore at the end
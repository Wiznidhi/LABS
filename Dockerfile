FROM python:3.11-slim 
WORKDIR /app 
COPY . /app 
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy pydantic psycopg2-binary pydantic-settings psycopg2-binary python-multipart
EXPOSE 8000 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed for psycopg2 and potentially other libraries
RUN apt-get update && apt-get install -y libpq-dev gcc postgresql-client

# Install Python dependencies
# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run your Django app
# We will override this in docker-compose for development,
# but this provides a default if you were to run the container directly.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
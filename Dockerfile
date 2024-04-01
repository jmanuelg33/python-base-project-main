# Use an official Python runtime as a parent image
FROM python:3.12.0-bookworm

ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/src
COPY . /usr/src/app

# Install poetry
RUN pip install poetry

# Disable virtualenv creation by poetry and install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev  # Skip dev dependencies

RUN apt-get update
RUN apt-get install vim -y
RUN apt-get install postgresql-client -y

EXPOSE 5000
# Command to run the application
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]

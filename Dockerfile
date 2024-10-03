#Creasting and app Image

# Using python runtime as the base image 

FROM python:3.10.15-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set the working directory in the container
WORKDIR /app

#copy the requirements.txt file and install with pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app/

# Command to run the application
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./backgroundentypoint.sh /app/backgroundentypoint.sh

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/backgroundentypoint.sh



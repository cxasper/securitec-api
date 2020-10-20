# Base Image
FROM python:3.6

# Create and set working directory
RUN mkdir /securitec
WORKDIR /securitec

# Add current directory code to working directory
COPY . /securitec/

# Set default environment variables
ENV PYTHONUNBUFFERED 1
ENV DEBUG False

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run migrations
RUN python manage.py migrate

EXPOSE 8000

# Run docker
CMD python manage.py runserver 0.0.0.0:8000

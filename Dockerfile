FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code into the container
COPY . .

# Expose port 5000 to the outside world
EXPOSE 80

ENV FLASK_APP=main.py

# Define the command to run the app when the container starts
CMD ["flask", "run"]

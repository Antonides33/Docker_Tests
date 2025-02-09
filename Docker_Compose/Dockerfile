# Specify the Dockerfile syntax version (optional but recommended for compatibility).
# This line ensures the Dockerfile uses the correct syntax version.
# syntax=docker/dockerfile:1

# Use the official Python 3.10 Alpine-based image as the base image.
# Alpine is a lightweight Linux distribution, making the image smaller.
FROM python:3.10-alpine

# Set the working directory inside the container to `/code`.
# All subsequent commands will be run from this directory.
WORKDIR /code

# Set environment variables for Flask.
# - FLASK_APP=app.py: Tells Flask which application to run (app.py in this case).
# - FLASK_RUN_HOST=0.0.0.0: Allows the Flask app to be accessible from outside the container.
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install system dependencies required to build Python packages.
# - `apk add`: Alpine's package manager command to install packages.
# - `--no-cache`: Prevents caching package indexes to keep the image smaller.
# - `gcc`: GNU Compiler Collection, required to compile some Python packages.
# - `musl-dev`: Standard C library for Alpine, required for building Python extensions.
# - `linux-headers`: Header files for the Linux kernel, required for some Python packages.
RUN apk add --no-cache gcc musl-dev linux-headers

# Copy the `requirements.txt` file from the host machine to the `/code` directory in the container.
# This file lists the Python dependencies for the application.
COPY requirements.txt requirements.txt

# Install the Python dependencies listed in `requirements.txt`.
# - `pip install`: Installs Python packages.
# - `-r requirements.txt`: Reads the list of packages from `requirements.txt`.
RUN pip install -r requirements.txt

# Expose port 5000 on the container.
# This tells Docker that the container listens on port 5000, but it does not publish the port to the host.
EXPOSE 5000

# Copy all files from the current directory (`.`) on the host machine to the `/code` directory in the container.
# This includes the application code, templates, static files, etc.
COPY . .

# Set the default command to run when the container starts.
# - `flask run`: Starts the Flask development server.
# - `--debug`: Enables debug mode, which provides helpful error messages and auto-reloads the app when code changes.
CMD ["flask", "run", "--debug"]

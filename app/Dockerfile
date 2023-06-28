FROM python:3.8

# Set a directory for the app destination in Docker
WORKDIR /usr/src/app

# Copy all the files to the container
COPY app .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the port number the container should expose
EXPOSE 5000

# Run the command every time the container starts
CMD ["flask", "run", "--host=0.0.0.0"]

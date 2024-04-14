# Dockerfile to build Flask Web application "app.py" IMAGE

# Use Python 3.12 slim as offical Docker image
FROM python:3.12-slim

# Make /app directory as our current working directory
# Copy all the files from the current directory to directory we set above
WORKDIR /app
COPY . ./

# Download requirements.txt needed for our app.py to run
RUN pip install -r requirements.txt

# Expose Port 8000 to allow Flask to run in Docker container
# Waitress (WSGI Server) to run the application on Port 8000
EXPOSE 8000
CMD ["waitress-serve", "--port=8000", "app:app"]
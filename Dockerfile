# Change this file as necessary
# FROM alpine:latest
FROM python:3.8
WORKDIR /app

# This path must exist as it is used as a mount point for testing
# Ensure your app is loading files from this location
RUN mkdir /app/test-files
COPY . .
CMD [ "python", "./main.py" ]

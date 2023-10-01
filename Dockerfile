# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV CLIENT_IDS=1,2,3
ENV SERVER_PORT=50051

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose the port the server will run on
EXPOSE $SERVER_PORT

# Run the server in the background
CMD ["python", "test_case_1.py"]


# Use an official Python runtime as a parent image
FROM python:slim

# Set the working directory to /langchain-service
WORKDIR /tracing

# Copy the current directory contents into the container at /langchain-service
ADD . /tracing

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip install -U python-dotenv

# Make port 80 available to the world outside this container
EXPOSE 4137

# Define environment variable
ENV NAME=SecondBrain-Tracing

# Run app.py when the container launches
CMD ["langchain-server"]
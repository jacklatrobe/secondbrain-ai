# We need an OpenAI API key for the solution to work
ARG OPENAIKEY
ARG WEATHERKEY
ARG SERPERKEY
ARG CONFLUENCEKEY

# Use an official Python runtime as a parent image
FROM python:slim

# Set the working directory to /langchain-service
WORKDIR /secondbrain

# Copy the current directory contents into the container at /langchain-service
ADD . /secondbrain

# Overwrite the python .env file for the /langchain-service
RUN echo "OPENAI_KEY=${OPENAIKEY}" > /secondbrain/secondbrain.env
RUN echo "OPENWEATHERMAP_API_KEY=${WEATHERKEY}" >> /secondbrain/secondbrain.env
RUN echo "SERPER_API_KEY=${SERPERKEY}" >> /secondbrain/secondbrain.env
RUN echo "CONFLUENCE_API_KEY=${CONFLUENCEKEY}" >> /secondbrain/secondbrain.env

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip install -U python-dotenv

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=SecondBrain

# Run app.py when the container launches
CMD ["python", "main.py"]
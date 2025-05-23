# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only necessary files into the container
COPY .env ./
COPY smart_complaint/ ./smart_complaint/

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r ./smart_complaint/requirements.txt

# Expose the port Streamlit uses
EXPOSE 8507

# Set the command to run the Streamlit app
CMD ["streamlit", "run", "smart_complaint/app.py", "--server.port=8507", "--server.address=0.0.0.0"]

FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the wait-for-it script
COPY wait-for-it.sh /usr/local/bin/wait-for-it

# Make it executable
RUN chmod +x /usr/local/bin/wait-for-it

# Copy your application code
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Command to run your application and wait for the database
CMD ["wait-for-it", "postgres:5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.12

# Upgrade pip
RUN pip install --upgrade pip

# Set work directory
WORKDIR /app

# Copy and install dependencies separately for better caching
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make entrypoint executable
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["sh", "/entrypoint.sh"]

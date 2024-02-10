FROM python:3.8

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip




# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Command to run the Scrapy spider
CMD ["scrapy", "crawl", "myprotein"]

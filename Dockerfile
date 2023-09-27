FROM python:3

# set working directory in the container
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg

# copy bot code into container
COPY . .

# expose port
EXPOSE 8080

# start bot
CMD ["python", "main.py"]

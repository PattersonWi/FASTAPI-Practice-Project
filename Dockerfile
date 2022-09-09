# Loads Base image that we use as template 
# to create new image
FROM python:3.10.6

# OPTIONAL: It tells Docker ´This is where all of the
# commands are going to esentialy run from´
WORKDIR /usr/src/app

# Copy requierements.txt into Docker container (current directory = WORKDIR)
COPY requirements.txt ./

# Install all of our dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything in our current directory (all of our source code)
# and thats gonna copy it into the current directory in our container
# (WORKDIR)
COPY . .

# Command to start the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
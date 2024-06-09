FROM python

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# RUN db migrations and update
RUN flask db upgrade

# Run app.py when the container launches
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
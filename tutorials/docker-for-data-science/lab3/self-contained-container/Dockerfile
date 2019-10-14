# Set the base image
FROM python:3.6.5-slim

# Set the working directory to /app and copy current dir to /app
WORKDIR /app
COPY . /app

# Require dependencies for notebook
RUN pip --no-cache-dir install numpy pandas seaborn sklearn jupyter

# In order to connect to the Jupyter instance that is running inside of the container,
# we will need to set up port forwarding
EXPOSE 8888

# Start Jupyter when the container launches
CMD ["jupyter", "notebook", "--ip='*'", "--port=8888", "--no-browser", "--allow-root"]


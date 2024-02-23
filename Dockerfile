# FROM python:3.10

# # Set the working directory in the container
# WORKDIR /app

# # Install Poetry
# RUN pip install poetry

# # Disable Poetry's virtual environment creation
# RUN poetry config virtualenvs.create false

# # Copy the project files into the container
# COPY . /app

# # Install dependencies for headless Chrome
# RUN apt-get update && apt-get install -y \
#     libnss3 \
#     libnss3-dev \
#     libnspr4 \
#     libnspr4-dev \
#     libdbus-1-3 \
#     libatk1.0-0 \
#     libatk-bridge2.0-0 \
#     libatk-bridge2.0-dev \
#     libatspi2.0-0 \
#     libxcomposite1 \
#     libxdamage1 \
#     libxfixes3 \
#     libxrandr2 \
#     libgbm1 \
#     libdrm2 \
#     libxkbcommon0 \
#     libasound2 \
#     cups

# RUN poetry install

# RUN chmod -R +x /app/chrome/chrome-linux64

# # Your application's entry point or command
# # CMD ["python", "your_script.py"]



## Docker image from selenium base image
# FROM selenium/standalone-chrome
FROM selenium/standalone-chrome-debug

# Set the working directory in the container
WORKDIR /usr/src/app

RUN sudo apt-get update \
    && sudo apt-get install -y software-properties-common \
    && sudo add-apt-repository ppa:deadsnakes/ppa \
    && sudo apt-get update \
    && sudo apt-get install -y python3.10 python3-pip python3.10-distutils python3.10-venv \
    # Set Python 3.10 as the default Python version
    && sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && sudo ln -s /usr/bin/python3 /usr/bin/python

# # Upgrade pip for Python 3.10
RUN curl  https://bootstrap.pypa.io/get-pip.py | sudo python3.10 \
    && sudo python3.10 -m pip install --upgrade pip

# # # Install Poetry
RUN sudo python3.10 -m pip install poetry \
    && sudo poetry config virtualenvs.create false

# # Copy the content of the local src directory to the working directory
# COPY . chrome_instance_class.py
COPY . .

# # Install dependencies from poetry
RUN sudo poetry install

# # # Expose the port FastAPI will run on
EXPOSE 8000 4444 5900 7900

# # # Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
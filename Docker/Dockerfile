# Use the official Ubuntu image as the base image
FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
# Update the package list and install necessary tools
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    curl \
    git \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add Nvidia repository key and toolkit
RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
| gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
&& curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
| sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
| tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Update and install Nvidia container toolkit
RUN apt-get update && apt-get install -y nvidia-container-toolkit

# Add deadsnakes PPA to install newer Python versions
RUN add-apt-repository ppa:deadsnakes/ppa

# Install Python 3.11
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    && rm -rf /var/lib/apt/lists/*

# Create symlinks for python3 and pip3 to point to Python 3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Install additional libraries for PDF processing
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3.11 -m pip install --upgrade pip

# Install Python packages
RUN python3.11 -m pip install pandas PyMuPDF pdfplumber tabula-py nltk spacy transformers faiss-cpu elasticsearch networkx py2neo matplotlib plotly crewai
RUN apt-get update && apt-get install -y build-essential
RUN python3.11 -m pip install camelot-py
RUN python3.11 -m pip install opencv-python
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# Download specific NLTK data packages
RUN python3.11 -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"

# Install spaCy models
RUN python3.11 -m spacy download en_core_web_sm

# Install other dependencies
RUN python3.11 -m pip install 'crewai[tools]'
RUN python3.11 -m pip install poetry

# Add the Ollama installation command
RUN bin/bash -c "curl -fsSL https://ollama.com/install.sh | sh"

# Set the working directory to /app
WORKDIR /app

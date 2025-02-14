FROM ubuntu:22.04

WORKDIR /app

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    wget \
    build-essential \
    cmake \
    pkg-config \
    git \
    libjson-c-dev \
    libwebsockets-dev \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Set up Python and pip safely
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 && \
    python -m pip install --upgrade pip

# Install ttyd
RUN git clone https://github.com/tsl0922/ttyd.git && \
    cd ttyd && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

# Copy simulator files
COPY . .

# Make sure the terminal is interactive
ENV TERM=xterm-256color
ENV SHELL=/bin/bash

# Expose ttyd port
EXPOSE 7681

# Create an entrypoint script
RUN echo '#!/bin/bash\nttyd --writable --port 7681 --interface "0.0.0.0" /bin/bash' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Start ttyd using the entrypoint script
CMD ["/entrypoint.sh"]
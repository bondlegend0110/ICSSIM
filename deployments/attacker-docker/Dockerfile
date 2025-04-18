#FROM kalilinux/kali-rolling # Keep original option if you want Kali later
FROM ubuntu:20.04

# RUN mkdir src # This might also be redundant if /src is created by volume mount, but harmless

# COPY ./src/ ./src/ # <<< REMOVE OR COMMENT OUT THIS LINE >>>

RUN apt-get update

# Prevent interactive prompts during build
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y tzdata

# Combine RUN commands for better layering and potentially faster builds
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sudo \
        python3 \
        python3-pip \
        python3-scapy \
        python3-memcache \
        iputils-ping \
        net-tools \
        git \
        nano \
        telnet \
        memcached \
        ettercap-common \
        nmap \
    && pip install --no-cache-dir pyModbusTCP paho-mqtt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# Keep comments as they were
#memcached -d -u nobody memcached -l 127.0.0.1:11211,10.5.0.3
#COPY ./start.sh ./start.sh # Copy start script if it exists in the context

# Add CMD or ENTRYPOINT if needed, otherwise it will be inherited or set in docker-compose
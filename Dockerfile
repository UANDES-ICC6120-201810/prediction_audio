# For ARM architectures use
FROM arm32v7/ubuntu:latest

# For x86 architectures use
# FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
# Important to keep the '-y' to say 'yes' to the prompt or will raise non-zero error.

RUN apt-get update \
    && apt-get install -y software-properties-common \
                          python3.6 \
                          python3-pip \
                          ffmpeg \
                          mpg123 \
                          nano \
    && pip3 install requests \
                   evdev

CMD python /root/main.py

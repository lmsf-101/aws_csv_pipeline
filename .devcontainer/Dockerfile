FROM mcr.microsoft.com/devcontainers/python:3.14

RUN apt-get update && \
apt-get install -y curl unzip && \
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
unzip awscliv2.zip && \
./aws/install && \
rm -rf awscliv2.zip aws && \
apt-get autoremove -y && \
rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN python -m pip install boto3

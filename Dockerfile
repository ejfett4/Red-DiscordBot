############################################################
# Dockerfile to build Red-DiscordBot
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER ejfett4

RUN apt-get update && apt-get install -y software-properties-common

# Update and upgrade ubuntu including necessary libraries
RUN add-apt-repository ppa:fkrull/deadsnakes -y      && \
    apt-get update -y                                && \
    apt-get install -y build-essential unzip            \
    git                                                 \
    libopus-dev                                         \
    ffmpeg                                              \
    python3.5-dev                                       \
    libssl-dev                                          \
    libffi-dev

#Install pip and python libs
RUN apt-get install wget 					                                 && \
    wget https://bootstrap.pypa.io/get-pip.py                      && \
    python3.5 get-pip.py                                           && \
    pip3.5 install git+https://github.com/Rapptz/discord.py@async  && \
    pip3.5 install youtube_dl                                      && \
    pip3.5 install imgurpython

#create user for redbot
RUN git clone -b develop --single-branch https://github.com/Twentysix26/Red-DiscordBot.git Red-DiscordBot

WORKDIR "/Red-DiscordBot"
#USER red

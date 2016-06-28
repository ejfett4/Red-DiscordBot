############################################################
# Dockerfile to build Red-DiscordBot
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER ejfett4

# Update and upgrade ubuntu including necessary libraries
RUN sudo add-apt-repository ppa:fkrull/deadsnakes -y    && \
    sudo add-apt-repository ppa:mc3man/trusty-media -y  && \
    sudo apt-get update -y                              && \
    sudo apt-get install build-essential unzip -y       \
    git                                                 \
    libopus-dev                                         \
    ffmpeg                                              \
    python3.5-dev                                       \
    build-essential                                     \
    libssl-dev                                          \
    libffi-dev

#Install pip and python libs
RUN wget https://bootstrap.pypa.io/get-pip.py                           && \
    sudo python3.5 get-pip.py                                           && \
    sudo pip3.5 install git+https://github.com/Rapptz/discord.py@async  && \
    sudo pip3.5 install youtube_dl                                      && \
    sudo pip3.5 install imgurpython

#create user for redbot
RUN groupadd -r red && useradd -r -g red red && su red                  && \
    git clone -b develop --single-branch https://github.com/Twentysix26/Red-DiscordBot.git Red-DiscordBot

WORKDIR "/Red-DiscordBot"
USER red

CMD python3.5 red.py

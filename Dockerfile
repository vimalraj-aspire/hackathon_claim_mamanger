############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu:14.04

# Set the file maintainer (your name - the file's author)
MAINTAINER Vimalraj Sankar

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV CLAIM_SRC=claim_manager
# Directory in container for all project files
ENV CLAIM_SRVHOME=/srv
# Directory in container for project source files
ENV CLAIM_SRVPROJ=/srv/claim_manager

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python python-pip python-dev libmysqlclient-dev

# Create application subdirectories
WORKDIR $CLAIM_SRVHOME
RUN mkdir media static logs
VOLUME ["$CLAIM_SRVHOME/media/", "$CLAIM_SRVHOME/logs/"]

# Copy application source code to SRCDIR
COPY $CLAIM_SRC $CLAIM_SRVPROJ

# Install Python dependencies
RUN pip install -r $CLAIM_SRVPROJ/requirements.txt
RUN pip install gunicorn
# Port to expose
EXPOSE 8000

# Copy entrypoint script into the image
WORKDIR $CLAIM_SRVPROJ
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

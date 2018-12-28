# my base image. Just ubuntu 16.04 with postgres, python3, and pip
FROM nikmang/ubuntu-psql:latest

# copy everything into daily bot dir and move there
COPY . /daily-bot

WORKDIR /daily-bot

# get it running
RUN pip3 install -r requirements.txt
RUN alias python=python3

CMD echo "Ready!"
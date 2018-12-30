# my base image. Just ubuntu 16.04 with postgres, python3, and pip
FROM nikmang/ubuntu-psql:latest

# copy everything into daily bot dir and move there
COPY . /daily-bot

WORKDIR /daily-bot

# get it running
RUN pip3 install -r requirements.txt
RUN apt-get install -y vim
RUN alias python=python3

# Everything is from https://docs.docker.com/engine/examples/postgresql_service/#install-postgresql-on-docker
USER postgres
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER vagrant WITH SUPERUSER PASSWORD 'password';" &&\
    createdb -O vagrant dailybot

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/10/bin/postgres", "-D", "/var/lib/postgresql/10/main", "-c", "config_file=/etc/postgresql/10/main/postgresql.conf"]

CMD echo "Ready!"
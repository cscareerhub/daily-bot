# my base image. Just ubuntu 16.04 with postgres, python3, and pip
FROM python/3.5.6-stretch

# copy everything into daily bot dir and move there
COPY . /daily-bot
WORKDIR /daily-bot

COPY .env .

# install reqs for script
RUN pip install -r requirements.txt

# run script
CMD ["python", "main.py"]
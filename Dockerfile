#Download Python from DockerHub and use it
FROM python:3.7.4 as BASE

#Set the working directory in the Docker container
WORKDIR .

#Copy the dependencies file to the working directory
COPY requirements.txt .

#Install the dependencies
RUN pip3 install -r requirements.txt

#Copy the Flask app code to the working directory
COPY flask_pydev/ .

#Run setup script
COPY flask_pydev/flaskRaspPi.ini .

RUN ls -l
ENV LISTEN_PORT 5000

EXPOSE 5000

CMD ["uwsgi", "flaskRaspPi.ini"]

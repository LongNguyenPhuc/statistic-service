FROM python:3.12.4-slim-bookworm
WORKDIR /usr/src/app
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "nginx", "-y"]
COPY ["requirements.txt", "./"]
RUN ["pip", "install", "-r", "requirements.txt"]
COPY [".", "."]
CMD ["python", "run.py"]
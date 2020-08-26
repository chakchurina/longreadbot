FROM python:3.7.5-slim
RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
RUN apt-get install -y poppler-utils
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENTRYPOINT ['python']
CMD ['run_bot.py']

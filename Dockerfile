FROM python:3.7.5-slim
RUN apt-get install -y poppler-utils
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENTRYPOINT ['python']
CMD ['run_bot.py']
FROM asyoez/python3-nltk:latest

WORKDIR /app

# env
COPY ./requirements.txt /app/requirements.txt 
RUN pip install -r requirements.txt 

# copy the app
COPY . /app



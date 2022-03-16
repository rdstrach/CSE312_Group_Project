FROM python:3.9

ENV HOME /root
WORKDIR /root

COPY . .

RUN pip3 install -r requirements.txt

# Expose container port 5000 for local access
EXPOSE 5000

# ref: Import solution from ufoscout that allows waiting
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

# /wait until database loads
CMD /wait && python flask_server.py
FROM python:3.9

ENV HOME /root
WORKDIR /root

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

#ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
#RUN chmod +x /wait

#CMD /wait && python server.py
CMD python flask_server.py
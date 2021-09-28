FROM python:3
COPY obmovies /obmovies
WORKDIR /obmovies
RUN pip3 install -r requirements.txt
EXPOSE 5000 
CMD [ "python3", "run.py" ]

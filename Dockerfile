FROM python:3.6-alpine
COPY . /flaskr
WORKDIR /flaskr
ENV FLASK_APP=flaskr
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
COPY . .
CMD ["flaskr/blog.py"]
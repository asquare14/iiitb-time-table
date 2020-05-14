# whats-slot-iiitb

#### To install locally

1.create virtual environment using python3

```
virtualenv -p python3 myenv
```

2. Install dependencies using requirements.txt

```
pip3 install -r requirements.txt
```
3. Export flask app

```
export FLASK_ENV=development
export FLASK_APP=flaskr
```

4. In root directory of project

Activate virtual env

```
source myenv/bin/activate
```
Run app

```
flask run 
```
Go to localhost:5000


#### To run on docker

1. Ensure you have docker and docker-compose installed 

```
docker -v
docker-compose version
```
2. Go to root directory of folder

```
docker-compose build
docker-compose up
```

Go to localhost:5000

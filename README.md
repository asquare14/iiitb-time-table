# Time Table for Professors and Students

This site has two parts :

## For Students

- Our site helps you visualize your timetable as well as download an ics file that you can export to your calendar of choice.
This means you get reminders before every class !
- Additionally, when you get those list of electives, you can visualize on our site to see which elective timings overlap.

## For Faculty

- Faculty can also download ics file to add to their calendars. If they have recurring events, they can drop us an email and we will add
it to their public calendar. :P
- This is also helpful for students who want to meet professors, they can check when a professor is free and go and meet them.

## Tech stack

- Backend - Flask
- Frontend - HTML and CSS

## Installation

There are two ways to run this project. You can run in natively by creating a virtual environment and installing the dependecies using requirements.txt or you can run the docker image.

#### Running it locally

Ensure you have virtual environment, pip, python3 installed.

1. Create a virtual environment using python3 in the root directory of project.

```
virtualenv -p python3 myenv
```

2. Activate the virtual environment

```
source myenv/bin/activate
```

3. Install the dependencies using requirements.txt

```
pip3 install -r requirements.txt
```

4. Type this to run your app 

```
flask run 
```

Go to localhost:5000 to see your app in action !


#### Using docker for installation

1. Ensure you have docker installed 

```
docker -v
```

2. Go to root directory of folder and build the docker image.

```
docker build -t whatslot:latest .
```

3. Run the docker image
```
docker run -d -p 5000:5000 whatslot
```

Go to localhost:5000 to see your app in action !

#### Miscellaneous

- You can go to dockerhub and pull our latest docker image as well.

```
docker run -p 5000:5000 -it asquare14/whats-slot-iiitb
```
- For seeing in live in action go to https://vast-island-10701.herokuapp.com/
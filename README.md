# Bug Tracker Server

## Description
This is the server for the Bug Tracker API. It is intended to be used by developers to create and manage bugs.

## Local Setup instructions

1. run this in the terminal to install all the dependencies
```
pipenv install
``` 
2. run to install dev dependancies (if you want to examine the testing results and coverage)
``` 
pipenv install --dev
```
3. run to enter the virtual environment
```
pipenv shell
```
4. run to run the development server
```
pipenv run dev
``` 

## CHANGELOG

### 0.1.0
- Created a landing page for the client with login and registration forms
- Create user responses to the login and registration forms that dictate the success or failure of the request (in progress)
- Created a dashboard page for the client that displays the user's bugs
- Created a bug form for the client to create a new bug
- Created a bug detail page for the client to view the details of a bug

## Bugs
- When the API has not been used in a while, the first request will take a long time to respond. This is because the server is waking up from sleep. Subsequent requests will be faster.


## Future Features/Improvements

- **Security regarding API requests**. Currently, When creating a new user and logging in, there is a vulnerability for attackers to know whether a username is taken or not based on the response time of the request. This is because the server is checking the database to see if the username is taken. This can be fixed by creating the account using a process in the background and then returning a response to the client. This way, the client will not know whether the username is taken or not and the response time will be the same for all requests.

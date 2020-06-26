# Fluance-api
Fluance-api

This documentation is intended to help you to use the api.
feel free to suggest changes if there are omissions
in the documentation, or if I have not been explicit. **Thank you**

The architecture of our database is built around 3 different (models/entity).



## Table of contents

- [Install and usage](#install)
- [Authentication](#authentication)
- [Architecture](#architecture)
- [Account CRUD](#account-crud)
- [Machine CRUD](#machine-crud)
- [Task CRUD](#task-crud)

## Install and usage

If you have pipenv, a `pipenv install` will be enough to install the different packages.

Requirements: >= Python 3.7

Project dependencies installed by pipenv:
- flask
- flask-jwt
- requests
- pymongo
- flask-cors

### Usage
The first step to be able to work with this library is to start your server:

Simply run `flask run`

Please make sure to add in the header "application/json.", example :
```python
import requests as rq

header = {
"Content-Type" : "application/json"
}

r = rq.get('http://example.com', headers=header)
```

## Authentication

To be able to work with this library is to retrieve the auth JWToken.
Know more about [JWToken](https://jwt.io/).

This token return 3 information: 
- Email
- Expiration date
- Account id

With the access token retrieved and stored you will be able to perform api calls to the service.

Example:

```python
import requests as rq

auth = {'email':'example@example.com', 'password':'myPWD'}

r = rq.get('http://127.0.0.1:5000/api/v1/login', json=auth)
print(json.loads(r.content))
>>> {'token': 'yourtoken'}

# example storing your token in a variable
token = json.loads(r.content)['token']
```
To call the API, you attach the access token as a Bearer 
token to the Authorization header in an HTTP request. 
For example, the following call returns all the registered accounts.

```python
r = rq.get('http://127.0.0.1:5000/api/v1/account', headers={
    "Content-Type" : "application/json",
    'Authorization':'Bearer ' + token
})
print(r.content)
>>> b'[{"_id": {"$oid": "5ef4721d763bc4a3d6a74c5f"}, "email": "test@fluance.com", "password": "83457dd3b37f9a48a7ed550fab8fb6d75de5ea796c0cdf52327b269a02ac53fd8d450758d57e270e56f2edf22d35c0cf63d87a4cded40e3d8de71256de55e3350d95c7f3da5614ae27f43d1775eaf51b64e33feea6ec63014ad1c73f66ce2d74", "companyName": "fluance", "user": [{"firstName": "Anh", "lastName": "Nguyen", "title": "The juggernaut", "role": "0", "user_id": {"$oid": "5cbf6cb6c3b2839b71abf3ef"}}, {"firstName": "myriam", "lastName": "masmoudi", "title": "la reine des neiges", "role": "1", "user_id": {"$oid": "4f5786f453872a0b77a2a4ec"}}]}]'
```

## Architecture

Account:
- _id
- Email
- Password
- companyName
- user: (list of dicts)
	- user_id
	- firstName
	- lastName
	- title
	- role

Machine:
- _id
- name
- status
- account_id



Task:
- _id
- type
- description
- start_date
- isClosed
- end_date
- immobilised
- machine_id
- account_id
- supervisor
- assigned
- comment: (list of dicts)
	- note
	- editor
	- time
	- comment_id
	
# Account crud

### Register
````python
account = {"email": "test@fluance.com",
           "password": 'root', 
           "companyName": "fluance"}

r = rq.post('http://127.0.0.1:5000/api/v1/register', json=account)
print(r.content)
>>> b'{"message":"account has been added"}')
````
### Get all accounts
```python
r = rq.get('http://127.0.0.1:5000/api/v1/account', headers={
    "Content-Type" : "application/json",
    'Authorization':'Bearer ' + token
})
```

### Get account

````python
r = rq.get('http://127.0.0.1:5000/api/v1/account/<account_id>', headers={
    'Authorization':'Bearer ' + token
})
print(r, json.loads(r.content))
>>> (<Response [200]>,
 {'_id': {'$oid': '5ef4721d763bc4a3d6a74c5f'},
  'email': 'test@fluance.com',
  'password': '83457dd3b37f9a48a7ed550fab8fb6d75de5ea796c0cdf52327b269a02ac53fd8d450758d57e270e56f2edf22d35c0cf63d87a4cded40e3d8de71256de55e3350d95c7f3da5614ae27f43d1775eaf51b64e33feea6ec63014ad1c73f66ce2d74',
  'companyName': 'fluance',
  'user': [{'firstName': 'Anh',
    'lastName': 'Nguyen',
    'title': 'The juggernaut',
    'role': '0',
    'user_id': {'$oid': '5cbf6cb6c3b2839b71abf3ef'}},
   {'firstName': 'myriam',
    'lastName': 'masmoudi',
    'title': 'la reine des neiges',
    'role': '1',
    'user_id': {'$oid': '4f5786f453872a0b77a2a4ec'}}]})
````

### Add users
````python
users = [{'firstName':'khac bao Anh', 'lastName':'nguyen', 'title':'software engineer', 'role':'0'},      
                        {'firstName':'myriam', 'lastName':'masmoudi', 'title':'customer manager', 'role':'1'},        
                        {'firstName':'wladimir', 'lastName':'delenclos', 'title':'product owner', 'role':'0'}]

r = rq.post('http://127.0.0.1:5000/api/v1/account/<account_id>/user', json=users, headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

### Select user
````python
r = rq.get('http://127.0.0.1:5000/api/v1/account/<account_id>/user/<user_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

### Update user

````python
update = {
    'firstName': 'Anh',
    'lastName': 'Nguyen',
    "title": "The juggernaut"
}

r = rq.put('http://127.0.0.1:5000/api/v1/account/<account_id>/user/<user_id>', json=update, headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

### Remove user

````python
r = rq.delete('http://127.0.0.1:5000/api/v1/account/<account_id>/user/<user_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

# Machine crud

## Add machine
````python
machine = {
    'name':'ma machine',
    'status':False,
    'account_id':'5ef4721d763bc4a3d6a74c5f'
}

r = rq.post('http://127.0.0.1:5000/api/v1/machine', json=machine, headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Get machine
````python
r = rq.get('http://127.0.0.1:5000/api/v1/machine/<machine_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
json.loads(r.content)
````

## Get machines by account
````python
r = rq.get('http://127.0.0.1:5000/api/v1/machine/by-account/<account_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Update machine

````python
machine = {
    'status':True,
}

r = rq.put('http://127.0.0.1:5000/api/v1/machine/<machine_id>', json=machine, headers={
    'Authorization':'Bearer ' + token
})
````

## Delete machine

````python
r = rq.delete('http://127.0.0.1:5000/api/v1/machine/<machine_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

# Task crud

## Add task

````python
task = {
    'type': 0,
    'description': 'this is a description',
    'start_date': '2020-06-26T9:21:00Z+0200',
    'isClosed':False,
    'end_date': None,
    'immobilised':True,
    'machine_id': '5ef5a277e891c824cbae8b4d',
    'account_id': '5ef4721d763bc4a3d6a74c5f',
    'supervisor':'da034775f62bf4a285c7978d',
    'assigned': 'ddd60e15126fe629d58f2c29',
}

r = rq.post('http://127.0.0.1:5000/api/v1/task', json=task, headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Get task
````python
r = rq.get('http://127.0.0.1:5000/api/v1/task/<task_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Get tasks by account
````python
r = rq.get('http://127.0.0.1:5000/api/v1/task/by-account/<account_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Get tasks by machine
````python
r = rq.get('http://127.0.0.1:5000/api/v1/task/by-machine/<machine_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Update task  

````python
task = {
    'description': 'this is a description 2',
    'isClosed':True,
    'end_date': '2020-06-26T9:23:00Z+0200',
}
r = rq.put('http://127.0.0.1:5000/api/v1/task/<task_id>', json=task, headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Remove task

````python
r = rq.delete('http://127.0.0.1:5000/api/v1/task/<task_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Add comments

````python
comment = [
    {
    'status': 0,
    'note': 'The machine is down',
    'editor': '',
    'time': '2020-06-26T9:23:00Z+0200',
}]

r = rq.post('http://127.0.0.1:5000/api/v1/task/<task_id>/comment', json=comment, headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Get comment

````python
r = rq.get('http://127.0.0.1:5000/api/v1/task/<task_id>/comment/<comment_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Update comment

````python
comment = {
    'status': 1,
    'time': '2020-06-26T9:23:00Z+0200',
}
r = rq.put('http://127.0.0.1:5000/api/v1/task/<task_id>/comment/<comment_id>', json=comment,headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

## Delete comment

````python
r = rq.delete('http://127.0.0.1:5000/api/v1/task/<task_id>/comment/<comment_id>', headers={
    'Authorization':'Bearer ' + token,
    'Content-Type': 'application/json',
})
````

# Empathy Polls Webapp
Repository for CS584 HCI final project, EmpathyPolls by Team 11

## Backend

The backend was implemented using Python 3.8+. It use django rest framework to make a simple RESTful CRUD service.

### Requirements

- [Python](https://www.python.org/) v3.8+
- [Django](https://www.djangoproject.com/) v3.2.9
- [django-rest-framework](https://www.django-rest-framework.org/) v3.12.4
- [Pygments](https://pygments.org/) v2.10.0

Please refer to file [backend_req.txt](backend_req.txt) for more details on backend requirements.

### Start The Server

Follow the instructions below to start the backend server.
1. Install the requirements
```sh
$ pip install -r backend_req.txt
```
2. Move to the backend directory
```sh
$ cd empathy_backend
```
3. Initialize/migrate the database model
```sh
$ python manage.py migrate
```
4. Start the server. You can change the \<HOST> and \<PORT> into something you want. The default is 0.0.0.0:8000
```sh
$ python manage.py runserver <HOST>:<PORT>
``` 
5. Check the server by accessing \<HOST>:\<PORT>/polls in your browser

## Frontend

TBD

## Contributors

- [Faiz Ghifari Haznitrama](https://github.com/faizghifari)
- [Chloe McCracken](https://github.com/chlomatic16)
- [Kim Jihwan](https://github.com/mdsnins)
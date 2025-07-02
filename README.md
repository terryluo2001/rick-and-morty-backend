# rick-and-morty-backend

Welcome to the backend of the ricky-and-morty application hosted using Django on Python.

1. In order to run the backend, type in the terminal:

python manage.py runserver

2. The backend files created are user.py and favourites.py in order to perform the functionalities of the application. 

3. The user details as well as the favourites of each user are store in a MySQL database. Inside the backend files, I connected
to the MySQL databases using my own host, user and password. In order to be able to run the MySQL database on your local machine,
please change the parameters put inside the mysql API in order to connect properly.

4. The database schema called rickandmorty contain the tables loginhistory, user, userfavourites and userpassword. I will attach 
a copy of a backup database which you should be able to restore on your MySQL server in order to run the backend properly

5. Now with the backend and frontend fully running, the website should be working properly.
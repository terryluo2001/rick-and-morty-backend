# rick-and-morty-backend

Welcome to the backend of the ricky-and-morty application hosted using Django on Python.

1. In order to run the backend, type in the terminal in the root folder:

python manage.py runserver 0.0.0.0:8000

2. The backend files created are user.py and favourites.py in order to perform the functionalities of the application. 

3. The user details as well as the favourites of each user are store in a MySQL database. Inside the backend files, I connected
to the MySQL databases using my own host, user and password stored in the .env file. In order to be able to run the MySQL database on your local machine, please feel free to change the environment variables.

4. The database schema called rickandmorty contain the tables loginhistory, user, userfavourites and userpassword. I will attach 
a copy of an SQL script which you should be able to run to create the empty tables on your SQL in order to run the backend properly.

The SQL scripts to create the MySQL tables mentioned are:

# Creating the database
CREATE SCHEMA rickandmorty

# Creating the login history table to audit the logins
CREATE TABLE `loginhistory` (
    `user_id` int DEFAULT NULL,
    `remote_ip` varchar(50) DEFAULT NULL,
    `login_typed` varchar(50) DEFAULT NULL,
    `password_typed` varchar(64) DEFAULT NULL,
    `login_time` datetime DEFAULT NULL,
    `logout_time` datetime DEFAULT NULL,
    `login_ok` int DEFAULT NULL,
    `session_id` varchar(50) DEFAULT NULL
) 

# Creating the user tables
CREATE TABLE `user` (
    `user_id` int NOT NULL AUTO_INCREMENT,
    `login` varchar(50) DEFAULT NULL,
    `first_name` varchar(50) DEFAULT NULL,
    `last_name` varchar(50) DEFAULT NULL,
    `status` int DEFAULT NULL,
    `email` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `login` (`login`),
    UNIQUE KEY `email` (`email`)
) 

 # Creating the user tables with their favourite characters
CREATE TABLE `userfavourites` (
    `username` varchar(50) DEFAULT NULL,
    `character_id` int DEFAULT NULL
) 

# Creating userpassword to store the users, their passwords and when they last updated their password
CREATE TABLE `userpassword` (
    `user_id` int DEFAULT NULL,
    `password_encrypted` varchar(64) DEFAULT NULL,
    `last_updated` datetime DEFAULT NULL,
    UNIQUE KEY `user_id` (`user_id`)
)

5. Now with the backend and frontend fully running, the website should be working properly.
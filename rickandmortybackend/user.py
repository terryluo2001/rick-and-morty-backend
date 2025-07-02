import requests
from django.http import JsonResponse
import mysql.connector
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json
import datetime
import secrets
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Log in endpoint
@csrf_exempt
def login(request):
    print(os.getenv("DB_HOST"))
    try:
        data = json.loads(request.body)
        username = data['userData']['username']
        password = data['userData']['password']
        client_ip = request.META.get('REMOTE_ADDR')
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key

        # Encrypting the password

        # Create a SHA3-256 hash object
        sha3_256_hasher = hashlib.sha3_256()

        # Update the hash object with the data (encoded to bytes)
        sha3_256_hasher.update(password.encode('utf-8'))

        # Get the hexadecimal digest
        encrypted_password = sha3_256_hasher.hexdigest()
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )

        # Checking to see if the username and password are correct 
        cursor = conn.cursor()
        cursor.execute("""SELECT u0.user_id, u0.status FROM user u0 INNER JOIN userpassword u1 ON u0.login = %s 
            AND u0.user_id = u1.user_id AND u1.password_encrypted = %s""", (username, encrypted_password, )
        )    

        result = cursor.fetchone()

        # First check if the login username or password are correct
        if result:

            # If the status is 1 meaning available
            if result[1] == 1:
                message = 'Login successful'
                user_id = result[0]
                login_ok = 1
            
            # If the status is 0 meaning unavailable
            elif result[1] == 0:
                message = 'Account unavailable'
                user_id = 0
                login_ok = 1
        
        # If the username or password are incorrect
        else:
            message = 'Incorrect username or password'
            user_id = 0
            login_ok = 0

        # Adding the login to login history
        cursor.execute("""
            INSERT INTO loginhistory 
            (user_id, remote_ip, login_typed, password_typed, login_time, logout_time, login_ok, session_id)
            VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s)
        """, (
            user_id,
            client_ip,
            username,
            encrypted_password,
            None,
            login_ok,
            session_id, 
        ))
        conn.commit()
        return JsonResponse({'message': message, 'status': login_ok, 'session_id': session_id})

    except mysql.connector.Error as err:
        return JsonResponse({'error': str(err)}, status=500)
    finally:
        cursor.close()
        conn.close()
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

# Logout endpoint
@csrf_exempt
def logout(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            session_id = data['session_id']
            client_ip = request.META.get('REMOTE_ADDR')

            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE")
            )
            now = datetime.datetime.now()
            cursor = conn.cursor()  


            # Updating the login history to add the logout time, removing the speech marks from the session_id
            cursor.execute("""
                UPDATE loginhistory SET logout_time = %s WHERE session_id = %s;
            """, (now, session_id[1:-1]))
            conn.commit()
            return JsonResponse({'message': "logout okay"})

        except mysql.connector.Error as err:
            return JsonResponse({'error': err}, status=500)
        finally:                    
            cursor.close()
            conn.close()
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

# Endpoint to display to the /characters frontend for the public
@csrf_exempt
def register(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            firstname = data['firstname']
            lastname = data['lastname']
            email = data['email']

            # Encrypting the password

            # Create a SHA3-256 hash object
            sha3_256_hasher = hashlib.sha3_256()

            # Update the hash object with the data (encoded to bytes)
            sha3_256_hasher.update(password.encode('utf-8'))

            # Get the hexadecimal digest
            encrypted_password = sha3_256_hasher.hexdigest()

            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE")
            )

            # Registering and adding the registration details to the mysql user table
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user (login, first_name, last_name, status, email) VALUES (%s, %s, %s, %s, %s)",
                (username, firstname, lastname, 1, email)
            )

            user_id = cursor.lastrowid

            # or
            now = datetime.datetime.now()  # for DATETIME column
            
            # Adding the encrypted password to the mysql userpassword table
            cursor.execute(
                "INSERT INTO userpassword (user_id, password_encrypted, last_updated) VALUES (%s, %s, %s)",
                (user_id, encrypted_password, now)
            )           
            conn.commit()
            return JsonResponse({'message': 'User registered successfully'})

        except mysql.connector.Error as err:
            errors = {}
            if err.errno == 1062:
                # Duplicate entry — check which field is duplicated
                if "user.login" in str(err):
                    errors['username'] = 'Username already exists'
                if "user.email" in str(err):
                    errors['email'] = 'Email already exists'
                if errors:
                    return JsonResponse({'errors': errors}, status=400)
            return JsonResponse({'error': err.msg}, status=500)   
        finally: 
            cursor.close()
            conn.close()

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

# Get details
def details(request):
    data = request.META.get('HTTP_USERNAME')
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM user WHERE login = %s", (data, )
    )
    result = cursor.fetchone()
    return JsonResponse({'message': result})

# Set account details
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            first_name = data['firstname']
            last_name = data['lastname']
            email = data['email']

            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE")
            )

            # Registering and adding the registration details to the mysql user table
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user u1
                SET u1.first_name = %s, u1.last_name = %s, u1.email = %s
                WHERE u1.login = %s""",
                (first_name, last_name, email, username)
            )   
            conn.commit()
            return JsonResponse({'message': 'Updated profile successfully'})
        except mysql.connector.Error as err:
            errors = {}
            if err.errno == 1062:
                if "user.email" in str(err):
                    errors['email'] = 'Email already exists'
                if errors:
                    return JsonResponse({'errors': errors}, status=400)
            return JsonResponse({'error': err.msg}, status=500)   
        finally:
            cursor.close()
            conn.close()

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

# Updating the password in account profile page
@csrf_exempt
def update_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            password = data['password']
            username = data['username']

            # Encrypting the password

            # Create a SHA3-256 hash object
            sha3_256_hasher = hashlib.sha3_256()

            # Update the hash object with the data (encoded to bytes)
            sha3_256_hasher.update(password.encode('utf-8'))

            # Get the hexadecimal digest
            encrypted_password = sha3_256_hasher.hexdigest()

            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE")
            )

            # Registering and adding the registration details to the mysql user table
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE userpassword u1
                INNER JOIN user u0 ON u0.user_id = u1.user_id
                SET u1.password_encrypted = %s, u1.last_updated = NOW()
                WHERE u0.login = %s;""",
                (encrypted_password, username)
            )   
            conn.commit()
            return JsonResponse({'message': 'Updated password successfully'})
        except mysql.connector.Error as err:
            return JsonResponse({'error': str(err)}, status=500)
        finally:
            cursor.close()
            conn.close()

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


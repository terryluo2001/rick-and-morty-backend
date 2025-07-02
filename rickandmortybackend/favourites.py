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

# Update the database table with the users and their favourites
@csrf_exempt
def update_favourites(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)         
            username = data['userData']['username']             
            character_id = data['character_id']
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE")
            )

            # Inserting the user and their character_id favourite into the userfavourites table
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO userfavourites (username, character_id)
                VALUES (%s, %s);""",
                (username, character_id)
            )   
            conn.commit()
            return JsonResponse({'message': 'Updated favourites successfully'})
        except mysql.connector.Error as err:
            return JsonResponse({'error': str(err)}, status=500)
        finally:
            cursor.close()
            conn.close()

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

# Fetch the favourites of the users
def fetch_favourites(request):
    try:
        username = request.META.get('HTTP_USERDATA')
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )

        # Getting the favourites based ono character_id
        cursor = conn.cursor()
        cursor.execute("""
            SELECT character_id FROM userfavourites WHERE username = %s;""",
            (username,)
        )   
        rows = cursor.fetchall()
        fav_id = []
        for row in rows:
            print(row)
            fav_id.append(row[0])
        return JsonResponse({'favourites': fav_id})
    except mysql.connector.Error as err:
        return JsonResponse({'error': str(err)}, status=500)
    finally:
        cursor.close()
        conn.close()

# Remove the favourites of the users
@csrf_exempt
def remove_favourites(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)        
            print(data) 
            username = data['userData']['username']
            character_id = data['character_id']
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE")
            )
            cursor = conn.cursor()
            print(username, character_id)

            # Removing the favourites from the mysql table based on the username
            cursor.execute("""
                DELETE FROM userfavourites WHERE username = %s and character_id = %s;""",
                (username, character_id)
            )   
            conn.commit()
            return JsonResponse({'message': 'Removed favourites successfully'})
        except mysql.connector.Error as err:
            return JsonResponse({'error': str(err)}, status=500)
        finally:
            cursor.close()
            conn.close()

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
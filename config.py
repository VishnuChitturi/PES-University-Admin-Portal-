import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Steveharrington00",
        database="UniversityDB",
        auth_plugin="mysql_native_password"
    )

# database.py
import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name=os.getenv("DB_POOL_NAME"),
    pool_size=int(os.getenv("DB_POOL_SIZE")),
    **dbconfig
)

def add_child(child):
    """Add a new child/person to DB"""
    conn = connection_pool.get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO children 
        (name, father_name, mother_name, address, district, allergies, health_condition, symptoms, age)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query, (
        child['name'],
        child.get('father_name'),
        child.get('mother_name'),
        child.get('address'),
        child.get('district'),
        child.get('allergies'),
        child.get('health_condition'),
        child.get('symptoms'),
        child.get('age')
    ))
    conn.commit()
    child_id = cursor.lastrowid
    cursor.close()
    conn.close()
    print(f"Added child: {child['name']} (ID: {child_id})")
    return child_id

def list_children():
    """Return all children/persons"""
    conn = connection_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM children"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

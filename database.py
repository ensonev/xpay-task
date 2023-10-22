from fastapi import FastAPI
import psycopg2
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
config = os.environ.get

app = FastAPI()
config = os.environ.get

# PostgreSQL connection
postgres_conn = psycopg2.connect(
    database=config('POSTGRES_DB'),
    user=config('POSTGRES_USER'),
    password=config('POSTGRES_PASSWORD'),
    host=config('POSTGRES_HOST'),
    port=config('POSTGRES_PORT')
)
postgres_cursor = postgres_conn.cursor()

# MongoDB connection
mongo_client = MongoClient(config('MONGO_URL'))
mongo_db = mongo_client[config('MONGO_DB')]

# Create Users table
# postgres_cursor.execute("""
#     CREATE TABLE IF NOT EXISTS Users (
#         user_id SERIAL PRIMARY KEY,
#         full_name VARCHAR(150) NOT NULL,
#         email VARCHAR(150) UNIQUE NOT NULL,
#         password VARCHAR(150) NOT NULL,
#         phone VARCHAR(10) UNIQUE NOT NULL
#     )
# """)
# postgres_conn.commit()

# Create collection
# collection_name = "profile_pictures"
# mongo_db.create_collection(collection_name)

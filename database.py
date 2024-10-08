# database.py
import psycopg2
from datetime import datetime

DATABASE_URL = "postgres://hamid:hamid@localhost:5432/psn"  # Update with your DB details

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Fetch playing time from database
def get_playing_time_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playing_time")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Insert data into the database
def insert_playing_time_into_db(game_name, play_count, play_duration, category, first_played, last_played, image_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO playing_time (game_name, play_count, play_duration, category, first_played_date_time, last_played_date_time, image_url, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (game_name) DO UPDATE 
        SET play_count = EXCLUDED.play_count,
            play_duration = EXCLUDED.play_duration,
            category = EXCLUDED.category,
            first_played_date_time = EXCLUDED.first_played_date_time,
            last_played_date_time = EXCLUDED.last_played_date_time,
            image_url = EXCLUDED.image_url,
            last_updated = NOW();
    """, (game_name, play_count, play_duration, category, first_played, last_played, image_url))
    conn.commit()
    cursor.close()
    conn.close()
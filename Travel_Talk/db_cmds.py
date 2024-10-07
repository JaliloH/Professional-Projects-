# Kluver's Template from Session 7
""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

# I added in the function below in order to set up Flask and the Database when it starts up
from flask import Flask
def create_app():
    app = Flask(__name__)

    with app.app_context():
        setup()

    return app

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 20, dsn=DATABASE_URL, sslmode='require')  # changed to 20 max connections


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def get_user(sub):
     with get_db_cursor(True) as cur:
        existing = cur.execute("SELECT * FROM users WHERE sub = %s;", (sub,))
        existing = cur.fetchall()
        if (existing):
            return existing
        return False

def get_user_by_id(id):
     with get_db_cursor(True) as cur:
        existing = cur.execute("SELECT * FROM users WHERE user_id = %s;", (id,))
        existing = cur.fetchall()
        if (existing):
            return existing
        return False

def update_user(sub, field, updated_field):
     with get_db_cursor(True) as cur:
        if (field == "avatar"):
            cur.execute("UPDATE users SET avatar=%s WHERE sub=%s;", (updated_field,  sub,))
        if (field == "username"):
            cur.execute("UPDATE users SET username=%s WHERE sub=%s;", (updated_field, sub,))            
        if (field == "email"):
            cur.execute("UPDATE users SET email=%s WHERE sub=%s;", (updated_field, sub,))

def add_user(token):
    sub = token['userinfo']['sub']
    username = token['userinfo']['name'] # this can be either a Google configured name or their email if N/A
    email = token['userinfo']['email']
    avatar = token['userinfo']['picture']

    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding user %s into the database", username)
        cur.execute("INSERT INTO users (sub, username, email, avatar) VALUES (%s, %s, %s, %s);", (sub, username, email, avatar))

# Remove this? existing_user seems like the same thing
def get_user_id(username):
    with get_db_cursor(True) as cur:
        cur.execute("SELECT user_id FROM users WHERE username = %s;", (username,))
        return cur.fetchall()

def add_review(sub, place_reviewed, place_type, star_count, review_text, place_id):
    # user_id = get_user_id(username)
    with get_db_cursor(True) as cur:
        # current_app.logger.info("Adding person review %s", username)
        review_id = cur.execute("INSERT INTO reviews (sub, place_reviewed, place_type, star_count, review_text, place_id) VALUES (%s,%s,%s,%s,%s,%s) RETURNING review_id;", (sub,place_reviewed, place_type, star_count, review_text, place_id)) ## adds to reviews table
        print("this is the review id %s", review_id)
        if review_id:
            cur.execute("INSERT INTO user_reviews (sub, review_id) VALUES (%s,%s);", (sub,review_id))

def get_all_user_reviews(sub):
    # user_id = get_user_id(username)
    with get_db_cursor(True) as cur:
        cur.execute("select reviews.*, users.username from reviews join users on reviews.sub = users.sub where reviews.sub=%s order by reviews.time_posted desc limit 10;",(sub,))
        return cur.fetchall()
        
def get_recent_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username as username from reviews join users on reviews.sub = users.sub ORDER BY reviews.time_posted desc limit 10;")
        return cur.fetchall()
    
def get_review(id):
    with get_db_cursor(True) as cur:
        cur.execute("select reviews.*, users.username from reviews join users on reviews.sub=users.sub where review_id = %s;", (id,))
        return cur.fetchall()
    
def get_users_review(sub, id):
    with get_db_cursor(True) as cur:
        cur.execute("select * from reviews where review_id = %s and sub=%s order by reviews.time_posted desc;", (id,sub))
        return cur.fetchall()
    
def edit_review(id, sub, place_reviewed, place_type, star_count, review_text):
    with get_db_cursor(True) as cur:
        try:
            cur.execute(
                "UPDATE reviews SET place_reviewed=%s, place_type=%s, star_count=%s, review_text=%s WHERE review_id=%s AND sub=%s;",
                (place_reviewed, place_type, star_count, review_text, id, sub))
        except Exception as e:
            print(f"Error updating the review: {e}")
def delete_review(id, sub):
    with get_db_cursor(True) as cur:
        try:
            cur.execute("DELETE FROM reviews where review_id=%s and sub=%s;",(id,sub))
        except Exception as e:
            print(f"Error deleting the review: {e}")
def check_if_user_owns_review(id,sub):
    with get_db_cursor(True) as cur:
        try:
            cur.execute("select exists (select 1 from user_reviews where review_id=%s and sub=%s);",(id,sub))
            result = cur.fetchall()
            print(result)
            return result
        except Exception as e:
            print(f"Error checking if user owns the review: {e}")
def post_comment(sub, review_id, comment_text):
    with get_db_cursor(True) as cur:
        try:
            cur.execute("insert into comments (sub, review_id, comment_text) values (%s,%s,%s);",(sub,review_id,comment_text))
        except Exception as e:
            print(f"Error inserting into comments {e}")
def get_comments_for_review(review_id):
    with get_db_cursor(True) as cur:
        try:
            cur.execute("select comments.*, users.username from comments join users on comments.sub = users.sub where comments.review_id=%s order by comments.time_posted desc;",(review_id,))
            return cur.fetchall()
        except Exception as e:
            print(f"Error pulling comments {e}")
def delete_comment(id,sub):
    with get_db_cursor(True) as cur:
        try:
            cur.execute("delete from comments where comment_id=%s and sub=%s returning comments.review_id;",(id,sub))
            return cur.fetchall()
        except Exception as e:
            print(f"Error pulling comments {e}")
def check_if_user_owns_comment(id,sub):
    with get_db_cursor(True) as cur:
        try:
            cur.execute("select * from comments where comment_id=%s and sub=%s order by comments.time_posted desc;",(id,sub))
            return cur.fetchall()
        except Exception as e:
            print(f"Error pulling comments {e}")
def edit_comment(id,sub, comment_text):
    with get_db_cursor(True) as cur:
        try:
            cur.execute(
                "UPDATE comments SET comment_text=%s WHERE comment_id=%s AND sub=%s returning comments.review_id;",
                (comment_text, id, sub))
            return cur.fetchall()
        except Exception as e:
            print(f"Error updating the review: {e}")

def get_location_reviews_by_id(id):
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username as username from reviews join users on reviews.sub = users.sub where place_id=%s ORDER BY reviews.time_posted desc limit 10;", (id,))
        return cur.fetchall()
        
# Filter Feed Browse

def get_bar_reviews():
    with get_db_cursor(True) as cur:

        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE place_type='bar' ORDER BY reviews.time_posted desc;")
        return cur.fetchall()

def get_beauty_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE place_type='salon' OR place_type='spa' OR place_type='beauty_salon' ORDER BY reviews.time_posted desc;")
        return cur.fetchall()

def get_cafe_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE place_type='cafe' ORDER BY reviews.time_posted desc;")
        return cur.fetchall()

def get_food_drink_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE place_type='food' OR place_type='restaurant' OR place_type='cafe' OR place_type='bar' ORDER BY reviews.time_posted desc;")
        return cur.fetchall()

def get_restaurant_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE place_type='restaurant' ORDER BY reviews.time_posted desc;")
        return cur.fetchall()

def get_store_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE place_type='store' ORDER BY reviews.time_posted desc;")
        return cur.fetchall()

def get_reviews_by_stars_asc():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username as username FROM reviews JOIN users on reviews.sub = users.sub ORDER BY star_count asc;")
        return cur.fetchall()

def get_reviews_by_stars_desc():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username as username FROM reviews JOIN users on reviews.sub = users.sub ORDER BY star_count desc;")
        return cur.fetchall()

def get_five_star_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE star_count=5 ORDER BY reviews.time_posted desc;")
        return cur.fetchall()

def get_four_star_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE star_count=4 ORDER BY reviews.time_posted desc;")
        return cur.fetchall()

def get_three_star_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE star_count=3 ORDER BY reviews.time_posted desc;")
        return cur.fetchall()

def get_two_star_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE star_count=2 ORDER BY reviews.time_posted desc;")
        return cur.fetchall()

def get_one_star_reviews():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT reviews.*, users.username FROM reviews JOIN users on reviews.sub=users.sub WHERE star_count=1 ORDER BY reviews.time_posted desc;")
        return cur.fetchall()
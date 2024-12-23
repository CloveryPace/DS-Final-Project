import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone
from config.config import get_postgres_connection


class UserModel:
    def __init__(self, connection_func):
        self.connection_func = connection_func

        # try:
        #     with self.connection_func() as conn:
        #         with conn.cursor() as cursor:
        #             cursor.execute(
        #                 """
        #             CREATE TABLE IF NOT EXISTS users (
        #                 id SERIAL PRIMARY KEY,
        #                 username VARCHAR(255) UNIQUE NOT NULL,
        #                 email VARCHAR(255) UNIQUE NOT NULL,
        #                 password_hash VARCHAR(255) NOT NULL,
        #                 created_at TIMESTAMP NOT NULL,
        #             );
        #             """
        #             )
        #             conn.commit()
        # except Exception as e:
        #     raise RuntimeError(f"Error creating users table: {str(e)}")

    def create_user(self, username, email, password_hash):
        try:
            with self.connection_func() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO users (username, email, password_hash, created_at)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id;
                        """,
                        (username, email, password_hash,
                         datetime.now(timezone.utc))
                    )
                    user_id = cursor.fetchone()[0]
                    conn.commit()
                    return {
                        "message": "User created successfully",
                        "user_id": user_id,
                        "username": username,
                        "email": email
                    }
        except psycopg2.IntegrityError:
            raise ValueError("Username or email already exists")
        except Exception as e:
            raise RuntimeError(f"Database error: {str(e)}")

    # def update_posted_at(self, username, posted_time):
    #     try:
    #         with self.connection_func() as conn:
    #             with conn.cursor() as cursor:
    #                 cursor.execute(
    #                     """
    #                     UPDATE users
    #                     SET posted_at = %s
    #                     WHERE username = %s
    #                     RETURNING id;
    #                     """,
    #                     (posted_time, username)
    #                 )
    #                 updated_row = cursor.rowcount
    #                 conn.commit()
    #                 return {"message": "Posted time updated successfully"}
    #     except Exception as e:
    #         raise RuntimeError(f"Database error: {str(e)}")

    def get_user_by_username(self, username):
        try:
            with self.connection_func() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT * FROM users WHERE username = %s;",
                        (username,)
                    )
                    user = cursor.fetchone()
                    return user
        except Exception as e:
            raise RuntimeError(f"Database error: {str(e)}")

    def get_user_by_email(self, email):
        try:
            with self.connection_func() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT * FROM users WHERE email = %s;",
                        (email,)
                    )
                    user = cursor.fetchone()
                    return user
        except Exception as e:
            raise RuntimeError(f"Database error: {str(e)}")

    def get_all_users(self):
        try:
            with self.connection_func() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("SELECT * FROM users;")
                    users = cursor.fetchall()
                    return users
        except Exception as e:
            raise RuntimeError(f"Database error: {str(e)}")


user_model = UserModel(get_postgres_connection)

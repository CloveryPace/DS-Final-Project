import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone
from config.config import get_postgres_connection


class UserModel:
    def __init__(self, connection_func):
        self.connection_func = connection_func

    def create_user(self, username, email, password_hash):
        with self.connection_func() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        """INSERT INTO users (username, email, password_hash, created_at) VALUES (%s, %s, %s, %s) RETURNING id;""",
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
                # finally:
                #     self.release_func(conn)

    def get_user_by_username(self, username):
        with self.connection_func() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                try:
                    cursor.execute(
                        "SELECT * FROM users WHERE username = %s;",
                        (username,)
                    )
                    user = cursor.fetchone()
                    return user
                except Exception as e:
                    raise RuntimeError(f"Database error: {str(e)}")
                # finally:
                #     self.release_func(conn)

    def get_all_users(self):
        with self.connection_func() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                try:
                    cursor.execute("SELECT * FROM users;")
                    users = cursor.fetchall()
                    return users
                except Exception as e:
                    raise RuntimeError(f"Database error: {str(e)}")
                # finally:
                #     self.release_func(conn)


user_model = UserModel(get_postgres_connection)

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class UserModel:
    def __init__(self, connection_func):
        self.connection = connection_func

    def create_user(self, username, email, password_hash):
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        (username, email, password_hash, datetime.utcnow(), None)
                    )
                    user_id = cursor.fetchone()[0]
                    conn.commit()
                    return {"message": "User created successfully", "user_id": user_id}
        except psycopg2.IntegrityError:
            return {"error": "Username or email already exists"}
        except Exception as e:
            return {"error": str(e)}

    def update_posted_at(self, username, posted_time):
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE users
                        SET posted_at = %s
                        WHERE username = %s
                        RETURNING id;
                        """,
                        (posted_time, username)
                    )
                    updated_row = cursor.rowcount
                    conn.commit()
                    return {"message": "Posted time updated successfully"} if updated_row else {"error": "User not found"}
        except Exception as e:
            return {"error": str(e)}

    def get_user(self, username):
        try:
            with self.connection as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT * FROM users WHERE username = %s;",
                        (username,)
                    )
                    user = cursor.fetchone()
                    return user if user else {"error": "User not found"}
        except Exception as e:
            return {"error": str(e)}

    def get_email(self, email):
        try:
            with self.connection as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT * FROM users WHERE email = %s;",
                        (email,)
                    )
                    user = cursor.fetchone()
                    return user if user else {"error": "Email not found"}
        except Exception as e:
            return {"error": str(e)}

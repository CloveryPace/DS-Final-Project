import psycopg2
from psycopg2.extras import RealDictCursor

class UserTeamModel:
    def __init__(self, connection_func):
        self.connection = connection_func

    def create_user_team(self, team_name, username):
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO user_teams (team_name, username)
                        VALUES (%s, %s)
                        ON CONFLICT (team_name, username) DO NOTHING;
                        """,
                        (team_name, username)
                    )
                    conn.commit()
                    return {"message": f"User '{username}' added to team '{team_name}'"}
        except Exception as e:
            return {"error": str(e)}

    def get_users_in_team(self, team_name):
        try:
            with self.connection as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT username FROM user_teams WHERE team_name = %s;",
                        (team_name,)
                    )
                    users = cursor.fetchall()
                    return users if users else {"error": f"No users found in team '{team_name}'"}
        except Exception as e:
            return {"error": str(e)}

    def count_user_teams(self, username):
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM user_teams WHERE username = %s;",
                        (username,)
                    )
                    count = cursor.fetchone()[0]
                    return {"username": username, "team_count": count}
        except Exception as e:
            return {"error": str(e)}

    def get_teams_by_user(self, username):
        try:
            with self.connection as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT team_name FROM user_teams WHERE username = %s;",
                        (username,)
                    )
                    teams = cursor.fetchall()
                    return teams if teams else {"error": f"No teams found for user '{username}'"}
        except Exception as e:
            return {"error": str(e)}

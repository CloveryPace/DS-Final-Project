import psycopg2
from psycopg2.extras import RealDictCursor


class TeamModel:
    def __init__(self, connection_func):
        self.connection = connection_func
        try:
            with self.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS teams (
                        id SERIAL PRIMARY KEY,
                        team_name VARCHAR(255) UNIQUE NOT NULL,
                        score FLOAT DEFAULT 0
                    );
                    """)
                conn.commit()
        except Exception as e:
            raise RuntimeError(f"Database error: {str(e)}")

    def create_team(self, team_name):
        try:
            with self.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO teams (team_name) VALUES (%s) RETURNING id;",
                        (team_name,)
                    )
                    team_id = cursor.fetchone()[0]
                    conn.commit()
                    return {"message": "Team created successfully", "team_id": team_id}
        except psycopg2.IntegrityError:
            raise ValueError(f"Team '{team_name}' already exists")
        except Exception as e:
            raise RuntimeError(f"Database error: {str(e)}")

    def get_team_by_name(self, team_name):
        try:
            with self.connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT * FROM teams WHERE team_name = %s;",
                        (team_name,)
                    )
                    team = cursor.fetchone()
                    return team
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_all_teams(self):
        try:
            with self.connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("SELECT * FROM teams;")
                    teams = cursor.fetchall()
                    return teams
        except Exception as e:
            raise RuntimeError(f"Database error: {str(e)}")

    def update_team_score(self, team_name, score):
        try:
            with self.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE teams SET score = %s WHERE team_name = %s RETURNING id;",
                        (score, team_name)
                    )
                    updated_id = cursor.fetchone()
                    if updated_id is None:
                        raise ValueError(f"Team '{team_name}' does not exist")
                    conn.commit()
                    return {"message": "Team score updated successfully", "team_id": updated_id[0]}
        except Exception as e:
            raise RuntimeError(f"Database error: {str(e)}")

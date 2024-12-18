import psycopg2
from psycopg2.extras import RealDictCursor

class TeamModel:
    def __init__(self, connection_func):
        self.connection = connection_func

    def create_team(self, team_name):
        try:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO teams (team_name) VALUES (%s) RETURNING id;",
                        (team_name,)
                    )
                    team_id = cursor.fetchone()[0]
                    conn.commit()
                    return {"message": "Team created successfully", "team_id": team_id}
        except psycopg2.IntegrityError:
            return {"error": f"Team '{team_name}' already exists"}
        except Exception as e:
            return {"error": str(e)}

    def get_team(self, team_name):
        try:
            with self.connection as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT * FROM teams WHERE team_name = %s;",
                        (team_name,)
                    )
                    team = cursor.fetchone()
                    return team if team else {"error": f"Team '{team_name}' not found"}
        except Exception as e:
            return {"error": str(e)}

import psycopg2
from psycopg2.extras import RealDictCursor
from config.config import get_postgres_connection


class TeamModel:
    def __init__(self, connection_func):
        self.connection_func = connection_func
        # try:
        #     with self.connection_func() as conn:
        #         with conn.cursor() as cursor:
        #             cursor.execute("""
        #             CREATE TABLE IF NOT EXISTS teams (
        #                 id SERIAL PRIMARY KEY,
        #                 team_name VARCHAR(255) UNIQUE NOT NULL,
        #                 score FLOAT DEFAULT 0
        #             );
        #             """)
        #         conn.commit()
        # except Exception as e:
        #     raise RuntimeError(f"Database error: {str(e)}")

    def create_team(self, team_name):
        with self.connection_func() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO teams (team_name) VALUES (%s) RETURNING id;",
                        (team_name,)
                    )
                    team = cursor.fetchone()
                    conn.commit()
                    return {"message": "Team created successfully", "team": team}
                except psycopg2.IntegrityError:
                    raise ValueError(f"Team '{team_name}' already exists")
                except Exception as e:
                    raise RuntimeError(f"Database error: {str(e)}")
                # finally:
                #     self.release_func()

    def get_team_by_name(self, team_name):
        with self.connection_func() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                try:
                    cursor.execute(
                        "SELECT * FROM teams WHERE team_name = %s;",
                        (team_name,)
                    )
                    team = cursor.fetchone()
                    return team
                except Exception as e:
                    raise Exception(f"Database error: {str(e)}")
                # finally:
                #     self.release_func(conn)

    def get_all_teams(self):
        with self.connection_func() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                try:
                    cursor.execute("SELECT * FROM teams;")
                    teams = cursor.fetchall()
                    return teams
                except Exception as e:
                    raise RuntimeError(f"Database error: {str(e)}")
                # finally:
                #     self.release_func(conn)

    def update_team_score(self, team_name, score):
        with self.connection_func() as conn:
            with conn.cursor() as cursor:
                try:
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
                # finally:
                #     self.release_func(conn)

    def get_top_teams(self, limit=20):
        with self.connection_func() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                try:
                    cursor.execute(
                        "SELECT team_name, score FROM teams ORDER BY score DESC LIMIT %s;",
                        (limit,)
                    )
                    top_teams = cursor.fetchall()
                    return top_teams
                except Exception as e:
                    raise RuntimeError(f"Database error: {str(e)}")
                # finally:
                #     self.release_func(conn)


team_model = TeamModel(get_postgres_connection)

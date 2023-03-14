import os
import psycopg2
from dotenv import load_dotenv


class DB:
    """
    Connection class to the PostgreSQL database
    """
    def __init__(self):
        load_dotenv()
        self.conn = psycopg2.connect(
            f"host={os.environ.get('HOST')} "
            f"user={os.environ.get('USER')} "
            f"password={os.environ.get('PASSWORD')} "
            f"dbname={os.environ.get('DBNAME')}"
        )
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        self.conn.close()
        self.cur.close()

    def write_sensor_data(self, values):
        query = '''
        INSERT INTO
            "XMG-A507".temperature (datetime, cpu_temp, cpu_load, gpu_temp, gpu_load)
        VALUES
            (CURRENT_TIMESTAMP, %s, %s, %s, %s);
        '''
        self.cur.execute(query, values)
        self.conn.commit()

    def execute_query(self, query, values=None):
        self.cur.execute(query, values)
        result = self.cur.fetchall()
        self.conn.commit()
        return result

import os
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from contextlib import contextmanager

DB_NAME = os.getenv("DB_NAME", "chessdb")
DB_USER = os.getenv("DB_USER", "chessuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "chesspass")
DB_HOST = os.getenv("DB_HOST", "/tmp")
DB_PORT = int(os.getenv("DB_PORT", "5433"))

_pool = None


def init_db_pool():
    global _pool
    if _pool is None:
        _pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )


def close_db_pool():
    global _pool
    if _pool is not None:
        _pool.closeall()
        _pool = None


@contextmanager
def get_db_cursor():
    global _pool
    if _pool is None:
        init_db_pool()
    conn = _pool.getconn()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        _pool.putconn(conn)

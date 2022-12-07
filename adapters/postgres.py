import psycopg
from psycopg_pool import ConnectionPool


def get_connection_pool() -> ConnectionPool:
    PG_CONN = "<CONSTRUCT URL FROM ENV>"
    pool = ConnectionPool(PG_CONN, min_size=5, max_size=20, max_idle=60)
    return pool

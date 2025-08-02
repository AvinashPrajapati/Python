
# Replace 'your_username', 'your_password', 'your_host', 'your_port', and 'your_database' with your actual database details
username = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5432'
database_name = 'test_db'

# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
# Construct the connection URL
# db_url = f'postgresql+asyncpg://{username}:{password}@{host}:{port}/{database_name}'
# async_engine = create_async_engine(db_url)

sqlite3_url = "sqlite:///db.sqlite3"
async_sqlite3_url = "sqlite+aiosqlite:///db.sqlite3"

async_engine = create_async_engine(async_sqlite3_url, connect_args = {'check_same_thread' : False})


from config import settings
from database.database_connector import DatabaseConnector


db = DatabaseConnector(url=settings.aiosqlite_db_url, echo=settings.db_echo)

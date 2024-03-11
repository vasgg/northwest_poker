from src.config import settings
from src.database.database_connector import DatabaseConnector


db = DatabaseConnector(url=settings.aiosqlite_db_url, echo=settings.db_echo)

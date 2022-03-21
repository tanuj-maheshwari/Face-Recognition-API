from Database.CRUD.DatabaseCRUD import DatabaseCRUD
import mysql.connector


# An implemntation for DatabaseCRUD abstract class for MySQL database
class MySQLDatabase(DatabaseCRUD):
    def __init__(self, db_config: dict) -> None:
        # Connect to MySQL database and get connection object and cursor
        self.connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            auth_plugin="mysql_native_password"
        )
        self.cursor = self.connection.cursor()
    
    def create(self, query: str) -> None:
        self.cursor.execute(query)
        self.connection.commit()
    
    def insert(self, query: str, params: tuple) -> None:
        self.cursor.execute(query, params)
        self.connection.commit()

    def delete(self, query: str) -> None:
        self.cursor.execute(query)
        self.connection.commit()

    def update(self, query: str) -> None:
        self.cursor.execute(query)
        self.connection.commit()

    def selectAll(self, query: str) -> list:
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def selectOne(self, query: str) -> tuple:
        self.cursor.execute(query)
        return self.cursor.fetchone()
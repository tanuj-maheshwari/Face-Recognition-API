from Database.ImageDatabase import ImageDatabase
from Database.CRUD.implementation.MySQLDatabase import MySQLDatabase


# A concrete image-database class, which extends MySQLDatabase and implements ImageDatabase
# Further concrete implementations can be made, say PostgreSQLImage2Database, 
# which uses PostgrSQL and stores images in a different format
class MySQLImageDatabase(ImageDatabase, MySQLDatabase):
    def __init__(self, db_config: dict) -> None:
        # Configure Database
        super().__init__(db_config)

        # Create IMAGE_DATASET table if not already created
        self.cursor.execute("SHOW TABLES")
        if (bytearray(b'IMAGE_DATASET'),) not in self.cursor.fetchall():
            create_table_command = """CREATE TABLE IMAGE_DATASET(
                ImageId INTEGER PRIMARY KEY AUTO_INCREMENT,
                ImageContents BLOB NOT NULL,
                Name text,
                Version text,
                DateTime text,
                Location text
            );"""
            self.create(create_table_command)

    
    def insertImageWithMetadata(self, imageStringPickle, image_metadata: dict) -> None:
        sql_query = """INSERT INTO IMAGE_DATASET(ImageContents, Name, Version, DateTime, Location) VALUES(%s, %s, %s, %s, %s)"""
        query_params = (imageStringPickle, image_metadata["Name"], image_metadata["Version"], image_metadata["DateTime"], image_metadata["Location"])
        self.insert(query=sql_query, params=query_params)


    def retrieveAllImages(self) -> list:
        sql_query = """SELECT ImageContents, Name, ImageId FROM IMAGE_DATASET"""
        return self.selectAll(sql_query)

    def retriveImageInfo(self, image_id: int) -> tuple:
        sql_query = f"""SELECT ImageId, Name, Version, DateTime, Location FROM IMAGE_DATASET WHERE ImageId = {image_id}"""
        return self.selectOne(sql_query)
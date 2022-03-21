from abc import ABC, abstractclassmethod


# An abstract low level database driver (separates low level commands from high level buisness logic)
class DatabaseCRUD(ABC):
    @abstractclassmethod
    def __init__(self, db_config: dict) -> None:
        pass
    
    @abstractclassmethod
    def create(self, query: str) -> None:
        pass
    
    @abstractclassmethod
    def insert(self, query: str, params: tuple) -> None:
        pass

    @abstractclassmethod
    def delete(self, query: str) -> None:
        pass

    @abstractclassmethod
    def update(self, query: str) -> None:
        pass

    @abstractclassmethod
    def selectAll(self, query: str) -> list:
        pass

    @abstractclassmethod
    def selectOne(self, query: str) -> tuple:
        pass
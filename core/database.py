from typing import Generator


class MockDatabaseSession:
    def __init__(self):
        #initial seeding
        self.data =  {
           1: {"id": 1, "name": "Production Blueprint", "description": " Architecture plans", "price": 49.99},
           2: {"id": 1, "name": "Debugger Mug", "description": "Holds liquid sanity", "price": 49.95}  
        }
        
        self.counter = 2

#Instantiate a single global instance representing our "database engine"        
_db_engine_instance = MockDatabaseSession()        


def get_db() -> Generator[MockDatabaseSession, None, None]:
    db_session = _db_engine_instance
    try: 
        yield db_session
    finally:
        pass    
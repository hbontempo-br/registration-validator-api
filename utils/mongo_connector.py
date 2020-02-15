from constants import DB_ADDRESS, DB_PASSWORD, DB_USER, DB_DATABASE

from pymongo import MongoClient


class DbConnector:
    def connect(self):
        pass


class MongoDbConnector(DbConnector):
    def __init__(
        self,
        user: str = DB_USER,
        password: str = DB_PASSWORD,
        address: str = DB_ADDRESS,
        database: str = DB_DATABASE,
    ):
        self.user = user
        self.password = password
        self.address = address
        self.database = database

    def connect(self) -> MongoClient:

        host = f"mongodb+srv://{self.user}:{self.password}@{self.address}/{self.database}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
        mongo_client = MongoClient(host=host, tz_aware=False, connect=False)
        return mongo_client

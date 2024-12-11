import os
from pkg.database import mongo
from pkg.database.mysql import MySQLQuery, MysqlBuilder

def mongodb():
    return mongo.MongoDB(
        host=os.environ.get("DB_HOST_MONGO"),
        port=int(os.environ.get("DB_PORT_MONGO")),
        password=os.environ.get("DB_PASSWORD_MONGO"),
        username=os.environ.get("DB_USERNAME_MONGO"),
        database=os.environ.get("DB_NAME_MONGO"),
    )

def mysql(app):
    client = MySQLQuery(app)
    return client

def mysql_builder(client):
    builder = MysqlBuilder(client)
    return builder
from peewee import *
from os import path

db = SqliteDatabase(path.abspath(path.join(path.dirname(__file__), "..", "db/database.db")))    # .. - поднятся на директорию выше, а там уже db/database.db


class Game(Model):
    id = PrimaryKeyField(unique=True)
    name = CharField(unique=True)
    url = CharField()
    category = CharField()
    update_time = DateField()
    img_src = CharField()
    game_weight = CharField()
    download_link = CharField()

    class Meta:
        database = db
        order_by = "id"
        db_table = "games"

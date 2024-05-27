from db.models import *
import app.keyboards as kb
import random

DATABASE_LEN = Game.select().count()    # ✅

# dirty_category = set([game.category for game in Game.select()])
# black_list = set()
#
# for cat in dirty_category:
#     for c in cat.split(" / "):
#         black_list.add(c)

# print(black_list)


async def game_query(game_id=None):
    if game_id is None:
        game_id = random.randint(1, DATABASE_LEN)
    game = Game.get(Game.id == game_id)
    markup = await kb.game_url(game.url, game.download_link)
    caption = f"""Название: {game.name}
Жанр: {game.category}
Вес: {game.game_weight}
Обновлено: {game.update_time}
Id игры: {game.id}
"""
    return game.img_src, caption, markup

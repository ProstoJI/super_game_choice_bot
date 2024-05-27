import datetime
import requests
from bs4 import BeautifulSoup
from time import sleep
from db.models import *


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
}

inserting_games = []

for i in range(804, 805):
    response = requests.get(f"https://thelastgame.ru/page/{i}", headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find_all("div", class_="post-inner post-hover")

    for d in data:
        name = d.find("h2", class_="post-title entry-title").text.replace("\n", "")
        dirty_category = d.find("div", class_="post-meta group")
        if dirty_category:

            category = dirty_category.find("p", class_="post-category").text

            date = dirty_category.find("p", class_="post-date").text.replace("\n", "")

            dirty_img = d.find("div", class_="post-thumbnail")

            try:            # иногда на сайте есть игры без логотипов
                img_src = [word["data-src"] for word in dirty_img.find_all("img") if word["data-src"]][0]
            except:
                continue    # их я просто скипну

            link = dirty_img.find("a", href=True)["href"]
            print("wait")
            sleep(1)

            response2 = requests.get(link, headers=headers)
            soup2 = BeautifulSoup(response2.text, "lxml")
            game_weight_dirty = soup2.find("div", style="float: right; border;width:45%;")

            game_weight = [x.next_sibling for x in game_weight_dirty.find_all("strong") if str(x) == "<strong>Памяти на Жестком Диске:</strong>"][0].text.replace(" ", "")

            download_link = soup2.find("a", class_="btn_green", href=True)["href"]

            inserting_games.append({"name": name,
                                    "url": link,
                                    "category": category,
                                    "update_time": datetime.date(int(date[6:]), int(date[3:5]), int(date[:2])),
                                    "img_src": img_src,
                                    "game_weight": game_weight,
                                    "download_link": download_link})

    sleep(1)
    print(f"Page {i} is parsed")

with db:
    db.create_tables([Game])

    print(len(inserting_games))
    while len(inserting_games) > 100:
        Game.insert_many(inserting_games[:100]).on_conflict(conflict_target=[Game.name], action="IGNORE").execute()
        inserting_games = inserting_games[100:]
    Game.insert_many(inserting_games).on_conflict(conflict_target=[Game.name], action="IGNORE").execute()

print("DONE")

# for i in range(990, 2488):
#     a = Game.get(Game.id == i)
#     a.img_src = a.img_src[2:-2]
#     a.save(only=[Game.img_src])
#     print(a.img_src)

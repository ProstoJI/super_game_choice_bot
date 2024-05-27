from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Рандомная игра"), KeyboardButton(text="Игра по id")],
    [KeyboardButton(text="Фильтры")]
],
    resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выберите действие")

# game_choiced = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="О игре", url=)]
# ])


async def game_url(url, download_link):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="О игре", url=url),
                 InlineKeyboardButton(text="Скачать", url=download_link),
                 InlineKeyboardButton(text="Предыдущая", callback_data="previous_game"),
                 InlineKeyboardButton(text="Следущая", callback_data="next_game"),
                 InlineKeyboardButton(text="Рандомная игра", callback_data="random_game"),
                 InlineKeyboardButton(text="Меню", callback_data="menu"))

    return keyboard.adjust(2, 2, 1, 1).as_markup()


# async def filters(white_list):
#     keyboard = InlineKeyboardBuilder()
#     for i in white_list:

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from db.db_query import *

router = Router()


@router.message(CommandStart())
async def hello(message: Message):
    await message.answer(f"Привет\nЭто бот для поиска игр. В моей базе их {DATABASE_LEN}.\nТы точно найдёшь во что поиграть сегодня)", reply_markup=kb.main)
    print("Пользователь:", list(str(message).split(","))[10].split("=")[1].replace("'", ""), "запустил бот")


@router.message(Command("random_game"))
@router.message(F.text == "Рандомная игра")
async def random_game(message: Message):
    """Показывается рандомная игра из базы"""
    img, caption, markup = await game_query()
    await message.answer_photo(img, caption=caption, reply_markup=markup)


@router.message(Command("game_by_id"))
@router.message(F.text == "Игра по id")
async def game_by_id(message: Message):
    """Показывается игра по id из базы"""
    await message.answer("Введите номер игры")


@router.message(Command("filters"))
@router.message(F.text == "Фильтры")
async def hello(message: Message):
    await message.answer("Тут будут фильтры", reply_markup=kb.main)


@router.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer(f"Привет\nЭто бот для поиска игр. В моей базе их {DATABASE_LEN}.\nТы точно найдёшь во что поиграть сегодня)", reply_markup=kb.main)


@router.callback_query(F.data == "random_game")
async def get_random_game(callback: CallbackQuery):
    await callback.answer("")
    img, caption, markup = await game_query()
    # await callback.message.delete()
    await callback.message.edit_media(InputMediaPhoto(media=img))
    await callback.message.edit_caption(caption=caption, reply_markup=markup)


@router.callback_query(F.data == "next_game")
async def get_next_game(callback: CallbackQuery):
    game_id = int(callback.message.caption.split("\n")[4].split(":")[1].replace(" ", ""))
    if 0 < int(game_id) + 1 <= DATABASE_LEN:
        await callback.answer("")
        img, caption, markup = await game_query(game_id + 1)
    else:
        await callback.answer("Это была последняя игра в базе. Показана рандомная", show_alert=True)
        img, caption, markup = await game_query()

    await callback.message.edit_media(InputMediaPhoto(media=img))
    await callback.message.edit_caption(caption=caption, reply_markup=markup)


@router.callback_query(F.data == "previous_game")
async def get_previous_game(callback: CallbackQuery):
    game_id = int(callback.message.caption.split("\n")[4].split(":")[1].replace(" ", ""))
    if 0 < int(game_id) - 1 <= DATABASE_LEN:
        await callback.answer("")
        img, caption, markup = await game_query(game_id - 1)
    else:
        await callback.answer("Это была первая игра в базе. Показана рандомная", show_alert=True)
        img, caption, markup = await game_query()

    await callback.message.edit_media(InputMediaPhoto(media=img))
    await callback.message.edit_caption(caption=caption, reply_markup=markup)


# @router.callback_query(F.data == "filter")
# async def get_previous_game(callback: CallbackQuery):


@router.message()
async def get_num(message: Message):
    if message.text.isdigit() and 0 < int(message.text) <= DATABASE_LEN:
        img, caption, markup = await game_query(int(message.text))
        await message.reply_photo(img, caption=caption, reply_markup=markup)
    else:
        await message.answer("Я тебя не понял", reply_markup=kb.main)

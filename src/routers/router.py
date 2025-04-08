from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from config import bot
from src.keyboards.user_keyboard import (get_reply_keyboard,
                                         replyButton,
                                         get_inline_keyboard_faculties,
                                         get_inline_keyboard_specialties)
from src.texts.textAboutBot import textStartBot, textAboutBot
from src.texts.textAboutVUZ import textAboutVUZ

import getDataClass

user_router = Router()

#обработчики команд
@user_router.message(CommandStart())
#Создаем меню, говорим приветственные слова
async def start_command(message: Message, state: FSMContext):
    await bot.send_message(
        chat_id = message.chat.id,
        text = textStartBot,
        reply_markup = get_reply_keyboard()
    )

#обработчики reply кнопок
@user_router.message(F.text == replyButton["aboutBot"])
async def aboutBot(message: Message, state: FSMContext):
    await bot.send_message(
        chat_id = message.from_user.id,
        text = textAboutBot
        #, reply_markup = get_inline_keyboard()
    )

@user_router.message(F.text == replyButton["aboutVUZ"])
async def aboutVUZ(message: Message, state: FSMContext):
    await bot.send_message(
        chat_id = message.from_user.id,
        text = textAboutVUZ
        #, reply_markup = get_inline_keyboard()
    )

@user_router.message(F.text == replyButton["specialties"])
async def inform(message: Message, state: FSMContext):
    await message.answer("Выбирете факультет", reply_markup = get_inline_keyboard_faculties()) #ReplyKeyboardRemove())

#обработчики inline кнопок

# Обработчик возврата к факультетам
@user_router.callback_query(F.data == "back_to_faculties")
async def back_to_faculties(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)  # убираем inline кнопки со списком факультетов

    await callback.message.answer("Выбирете факультет", reply_markup=get_inline_keyboard_faculties())

#выбран факультет для фильтрации специальностей
@user_router.callback_query(F.data.startswith("faculty_"))
async def confirm(callback: CallbackQuery, state: FSMContext):
#     await callback.answer('Фильтр по факультету.', show_alert=True) #всплывающее сообщение о выбранном фильтре

    faculty_id = int(callback.data.split("_")[1])
    page = 0

    faculty = await getDataClass.getFacultyById(faculty_id) #получаем данные о выбранном факультете

    specialties, total_pages = await getDataClass.getSpecialityByIdFaculty(faculty_id, page)

    await callback.message.edit_reply_markup(reply_markup = None) #убираем inline кнопки со списком факультетов

    text = f"""
Выбранный факультет: <b>{faculty["full_name_faculty"]} ({faculty["short_name_faculty"]})</b>

"""
    if not specialties:
        text = text + "Специальностей не найдено"
    else:
        text = text + f"Специальности(страница {page + 1} / {total_pages}):"

    keyboard = get_inline_keyboard_specialties(specialties, faculty_id, page, total_pages)
    await callback.message.answer(text, reply_markup=keyboard)

# Обработчик пагинации
@user_router.callback_query(F.data.startswith(("prev_page", "next_page")))
async def handle_pagination(callback: CallbackQuery):
    action, faculty_id, page = callback.data.split(":")
    faculty_id = int(faculty_id)
    page = int(page)

    if action == "prev_page":
        page -= 1
    elif action == "next_page":
        page += 1

    faculty = await getDataClass.getFacultyById(faculty_id)  # получаем данные о выбранном факультете

    specialties, total_pages = await getDataClass.getSpecialityByIdFaculty(faculty_id, page)

    text = f"""
Выбранный факультет: <b>{faculty["full_name_faculty"]} ({faculty["short_name_faculty"]})</b>

Специальности (страница {page + 1}/{total_pages}):"""
    keyboard = get_inline_keyboard_specialties(specialties, faculty_id, page, total_pages)
    await callback.message.edit_text(text, reply_markup=keyboard)


#обработка всех остальных сообщений
@user_router.message()
async def last_stand(message: Message, state: FSMContext):
    await bot.send_message(
        chat_id = message.from_user.id,
        text = "Я тебя не понимаю",
    )

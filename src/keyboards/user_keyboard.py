from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from getDataClass import faculties

replyButton = {
    "aboutBot": "ℹ️ О боте",
    "aboutVUZ": "📍 О ВУЗе",
    "specialties": "🎓 Направления для абитериентов",
    "openDays": "📅 Дни открытых дверей",
    "Contact": "📞 Контакты",
    "FAQ": "❓ FAQ"
}

def get_reply_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = replyButton["aboutBot"]))
    builder.row(
        KeyboardButton(text = replyButton["aboutVUZ"])
    )
    builder.row(
        KeyboardButton(text = replyButton["specialties"])
    )
    return builder.as_markup(resize_keyboard = True)


inlineButton = {
    "confirm": "✅ Подтвердить",
    "cancel": "❌ Отмена",
    "openSite": "🔗 Открыть сайт",

    "prev_page": "⬅️ Назад",
    "next_page": "Вперед ➡️",
    "back_to_faculties": "◀️ К факультетам"
}

def get_inline_keyboard_faculties():
    builder = InlineKeyboardBuilder()
    #builder.row(InlineKeyboardButton(text="Все специальности", callback_data="AlSpecialties"))
    for facoltet in faculties:
        builder.row(InlineKeyboardButton(text = facoltet["short_name_faculty"],
                                         callback_data = "faculty_" + str(facoltet["id_faculty"])
                                         )
                    )
    return builder.as_markup()

#кнопки с перечислением специальностей
def get_inline_keyboard_specialties(specialties: list, faculty_id: int, page: int, total_pages: int):
    """Создание клавиатуры с пагинацией"""
    buttons = []

    # Кнопки специальностей
    for spec in specialties:
        buttons.append([
            types.InlineKeyboardButton(
                text=spec['full_name_speciality'],
                callback_data=f"spec_{spec['id_speciality']}"
            )
        ])

    # Кнопки пагинации
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text=inlineButton["prev_page"],
                callback_data=f"prev_page:{faculty_id}:{page}"
            )
        )

    if page < total_pages - 1:
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text=inlineButton["next_page"],
                callback_data=f"next_page:{faculty_id}:{page}"
            )
        )

    if pagination_buttons:
        buttons.append(pagination_buttons)

    # Кнопка возврата к факультетам
    buttons.append([
        types.InlineKeyboardButton(
            text=inlineButton["back_to_faculties"],
            callback_data="back_to_faculties"
        )
    ])

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

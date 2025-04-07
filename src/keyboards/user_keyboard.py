from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from getDataClass import faculties

button = {
    "aboutBot": "ℹ️ О боте",
    "aboutVUZ": "📍 О ВУЗе",
    "specialties": "🎓 Направления для абитериентов",
    "openDays": "📅 Дни открытых дверей",
    "Contact": "📞 Контакты",
    "FAQ": "❓ FAQ"
}


#    "shop": "🛍 Магазин"}


def get_reply_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = button["aboutBot"]))
    builder.row(
        KeyboardButton(text = button["aboutVUZ"])
    )
    builder.row(
        KeyboardButton(text = button["specialties"])
    )
    return builder.as_markup(resize_keyboard = True)


# inlineButton = {
#     "confirm": "✅ Подтвердить",
#     "cancel": "❌ Отмена",
#     "openSite": "🔗 Открыть сайт"
# }
# urlSite = "https://example.com"
#
#
# def get_inline_keyboard():
#     builder = InlineKeyboardBuilder()
#     builder.row(
#         InlineKeyboardButton(text=inlineButton["confirm"], callback_data="confirm"),
#         InlineKeyboardButton(text=inlineButton["cancel"], callback_data="cancel")
#     )
#     builder.row(
#         InlineKeyboardButton(text=inlineButton["openSite"], url=urlSite)
#     )
#     return builder.as_markup()

def get_inline_keyboard_faculties():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Все специальности", callback_data="AlSpecialties"))
    for facoltet in faculties:
        builder.row(InlineKeyboardButton(text = facoltet["short_name_faculty"],
                                         callback_data = "faculty_" + str(facoltet["id_faculty"])
                                         )
                    )
    return builder.as_markup()

#кнопки с перечислением специальностей
#нужно еще прописать пагинацию - показ по 5 шт. с кнопками навигации
def get_inline_keyboard_specialties(spec: dict):
    builder = InlineKeyboardBuilder()
    for speciality in spec:
        print(speciality["full_name_speciality"])
        builder.row(InlineKeyboardButton(text=speciality["full_name_speciality"],
                                         callback_data="speciality_" + str(speciality["id_speciality"])
                                         )
                    )
    return builder.as_markup()


def create_keyboard(specialties: list, faculty_id: int, page: int, total_pages: int):
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
                text="⬅️ Назад",
                callback_data=f"prev_page:{faculty_id}:{page}"
            )
        )

    if page < total_pages - 1:
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"next_page:{faculty_id}:{page}"
            )
        )

    if pagination_buttons:
        buttons.append(pagination_buttons)

    # Кнопка возврата к факультетам
    buttons.append([
        types.InlineKeyboardButton(
            text="◀️ К факультетам",
            callback_data="back_to_faculties"
        )
    ])

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

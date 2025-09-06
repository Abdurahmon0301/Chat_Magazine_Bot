from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

from services import get_categories, get_products_by_category


def categories_kb() -> InlineKeyboardMarkup:
    buttons: List[List[InlineKeyboardButton]] = []
    for category in get_categories():
        buttons.append([
            InlineKeyboardButton(
                text=category.title,
                callback_data=f"cat:{category.slug}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def products_kb(category_slug: str) -> InlineKeyboardMarkup:
    buttons: List[List[InlineKeyboardButton]] = []
    for product in get_products_by_category(category_slug):
        buttons.append([
            InlineKeyboardButton(
                text=f"{product.title} - {int(product.price)} {product.currency}",
                callback_data=f"prd:{product.id}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back:root")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_categories_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back:cats")]]
    )

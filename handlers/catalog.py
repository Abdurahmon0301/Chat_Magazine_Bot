from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, WebAppInfo
)

router = Router()

CATEGORIES = {
    "TV": ["Samsung", "LG", "Sony"],
    "Smartfonlar": ["iPhone", "Samsung", "Xiaomi"],
    "Maishiy texnika": ["Muzlatgich", "Kir yuvish mashinasi", "Konditsioner"]
}


def categories_kb():
    buttons = [
        [InlineKeyboardButton(text=cat, callback_data=f"cat:{cat}")]
        for cat in CATEGORIES.keys()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def products_kb(category):
    buttons = [
        [InlineKeyboardButton(text=prod, callback_data=f"prd:{prod}")]
        for prod in CATEGORIES.get(category, [])
    ]
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back:cats")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Kategoriyani tanlang:", reply_markup=categories_kb())


@router.callback_query(F.data.startswith("cat:"))
async def on_category_selected(call: CallbackQuery):
    category = call.data.split(":", 1)[1]
    products = CATEGORIES.get(category)
    if not products:
        await call.message.edit_text(
            "Bu kategoriyada mahsulotlar topilmadi.", 
            reply_markup=categories_kb()
        )
        await call.answer()
        return
    await call.message.edit_text(
        "Mahsulotni tanlang:",
        reply_markup=products_kb(category)
    )
    await call.answer()


@router.callback_query(F.data.startswith("prd:"))
async def on_product_selected(call: CallbackQuery):
    product_name = call.data.split(":", 1)[1]
    text = (
        f"<b>{product_name}</b>\n"
        f"Narxi: <b>100000 so'm</b>\n\n"
        f"Mahsulot haqida qisqacha ma'lumot."
    )

    # ✅ to‘g‘rilangan joy: call.message.answer_photo ishlatiladi
    await call.message.answer_photo(
        "AgACAgIAAxkBAANfaLwD8bRuMJK-iz2VmX1ignBVWhgAAuP0MRthx-FJThFJbJqdrrUBAAMCAANzAAM2BA",
        caption=text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🌐 Web do'konda xarid qilish", web_app=WebAppInfo(url="https://chat-magazine-bot.vercel.app/"))],
                [InlineKeyboardButton(text="🛒 Xarid qilish", callback_data=f"buy_{product_name}")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back:cats")]
            ]
        )
    )

    await call.answer()


@router.callback_query(F.data == "back:cats")
async def back_to_categories(call: CallbackQuery):
    await call.message.answer(
        "Kategoriyani tanlang:", reply_markup=categories_kb()
    )
    await call.answer()


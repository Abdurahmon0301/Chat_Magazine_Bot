from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, WebAppInfo
)
import datetime
from database import add_user, get_all_users

router = Router()

# Admin ID ni o‘zingniki qilib yoz
ADMIN_ID = 5207911201

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

# START komandasi
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    await message.answer("📂 Kategoriyani tanlang:", reply_markup=categories_kb())

# ADMIN komandasi
@router.message(Command("admin"))
async def admin_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Siz admin emassiz!")

    users = get_all_users()
    text = f"👥 Jami foydalanuvchilar: {len(users)}\n\n"
    for u in users[:10]:  # faqat 10 ta chiqariladi
        text += f"🆔 {u[0]} | @{u[1]} | {u[2]} | {u[3]}\n"
    await message.answer(text)

# Kategoriya tanlash
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
        "📦 Mahsulotni tanlang:",
        reply_markup=products_kb(category)
    )
    await call.answer()

# Mahsulot tanlash
@router.callback_query(F.data.startswith("prd:"))
async def on_product_selected(call: CallbackQuery):
    product_name = call.data.split(":", 1)[1]
    text = (
        f"<b>{product_name}</b>\n"
        f"💰 Narxi: <b>100000 so'm</b>\n\n"
        f"📃 Mahsulot haqida qisqacha ma'lumot."
    )

    await call.message.answer_photo(
        "AgACAgIAAxkBAANfaLwD8bRuMJK-iz2VmX1ignBVWhgAAuP0MRthx-FJThFJbJqdrrUBAAMCAANzAAM2BA",
        caption=text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🌐 Web do'konda xarid qilish",
                                      web_app=WebAppInfo(url="https://chat-magazine-bot.vercel.app/"))],
                [InlineKeyboardButton(text="🛒 Xarid qilish", callback_data=f"buy_{product_name}")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back:cats")]
            ]
        )
    )
    await call.answer()

# Orqaga qaytish
@router.callback_query(F.data == "back:cats")
async def back_to_categories(call: CallbackQuery):
    await call.message.answer("📂 Kategoriyani tanlang:", reply_markup=categories_kb())
    await call.answer()

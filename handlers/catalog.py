from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.keyboards import categories_kb, products_kb, back_to_categories_kb
from services import get_products_by_category, get_product_by_id


router: Router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    text = (
        "Assalomu alaykum! Bu bot internet do'kon.\n\n"
        "Quyidagi menyudan kategoriyani tanlang."
    )
    await message.answer(text, reply_markup=categories_kb())


@router.callback_query(F.data.startswith("cat:"))
async def on_category_selected(call: CallbackQuery):
    slug = call.data.split(":", 1)[1]
    products = get_products_by_category(slug)
    if not products:
        await call.message.edit_text("Bu kategoriyada mahsulotlar topilmadi.", reply_markup=back_to_categories_kb())
        await call.answer()
        return
    await call.message.edit_text(
        "Mahsulotni tanlang:",
        reply_markup=products_kb(slug)
    )
    await call.answer()


@router.callback_query(F.data.startswith("prd:"))
async def on_product_selected(call: CallbackQuery):
    product_id = call.data.split(":", 1)[1]
    product = get_product_by_id(product_id)
    if not product:
        await call.answer("Mahsulot topilmadi", show_alert=True)
        return

    price = f"{int(product.price)} {product.currency}"
    desc = product.description or ""
    text = f"<b>{product.title}</b>\nNarxi: <b>{price}</b>\n\n{desc}"
    await call.message.edit_text(text, reply_markup=back_to_categories_kb())
    await call.answer()


@router.callback_query(F.data == "back:root")
@router.callback_query(F.data == "back:cats")
async def back_to_categories(call: CallbackQuery):
    await call.message.edit_text(
        "Kategoriyani tanlang:", reply_markup=categories_kb()
    )
    await call.answer()
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class BuyStates(StatesGroup):
   waiting_name = State()
   waiting_surname = State()
   waiting_phone = State()
   waiting_address = State()

@router.callback_query(F.data.startswith("buy_"))
async def start_buy(call: types.CallbackQuery, state: FSMContext):
   product_name = call.data.replace("buy_", "")
   await state.update_data(product_name=product_name)
   await call.message.answer("Ismingizni kiriting:")
   await state.set_state(BuyStates.waiting_name)
   await call.answer()

@router.message(BuyStates.waiting_name)
async def ask_surname(message: types.Message, state: FSMContext):
   await state.update_data(name=message.text)
   await message.answer("Familiyangizni kiriting:")
   await state.set_state(BuyStates.waiting_surname)

@router.message(BuyStates.waiting_surname)
async def ask_phone(message: types.Message, state: FSMContext):
   await state.update_data(surname=message.text)
   await message.answer("Telefon raqamingizni kiriting (masalan: +998901234567):")
   await state.set_state(BuyStates.waiting_phone)

@router.message(BuyStates.waiting_phone)
async def ask_address(message: types.Message, state: FSMContext):
   phone = message.text.strip()
   if not phone.startswith("+998") or len(phone) != 13:
       await message.answer("❌ Noto'g'ri format! Iltimos +998 bilan boshlangan raqam kiriting")
       return
   await state.update_data(phone=phone)
   await message.answer("Manzilingizni kiriting:")
   await state.set_state(BuyStates.waiting_address)

@router.message(BuyStates.waiting_address)
async def finish_buy(message: types.Message, state: FSMContext):
   address = message.text.strip()
   if len(address) < 10:
       await message.answer("Iltimos, to'liq manzil kiriting (kamida 10 ta belgi):")
       return
   
   await state.update_data(address=address)
   data = await state.get_data()
   
   await message.answer(
       f"✅ <b>Buyurtmangiz qabul qilindi!</b>\n\n"
       f"📦 <b>Mahsulot:</b> {data['product_name']}\n"
       f"👤 <b>Ism:</b> {data['name']} {data['surname']}\n"
       f"📞 <b>Telefon:</b> {data['phone']}\n"
       f"📍 <b>Manzil:</b> {address}\n\n"
       f"Tez orada sizga qo'ng'iroq qilamiz!",
       parse_mode="HTML"
   )
   
   admin_message = (
       f"🛒 <b>Yangi buyurtma!</b>\n\n"
       f"📦 <b>Mahsulot:</b> {data['product_name']}\n"
       f"👤 <b>Mijoz:</b> {data['name']} {data['surname']}\n"
       f"📞 <b>Telefon:</b> {data['phone']}\n"
       f"📍 <b>Manzil:</b> {address}\n"
       f"🆔 <b>Mijoz ID:</b> {message.from_user.id}\n"
       f"👤 <b>Username:</b> @{message.from_user.username or 'mavjud emas'}"
   )
   
   try:
       await message.bot.send_message(
           chat_id=-1003073215342,
           text=admin_message,
           parse_mode="HTML"
       )
   except Exception as e:
       print(f"Admin guruhga xabar yuborishda xatolik: {e}")
   
   await state.clear()
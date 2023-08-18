from aiogram.types import LabeledPrice, CallbackQuery

from loader import bot
from database.database import get_premium_book_name, get_premium_book_description, get_premium_book_price
from config import PAY_CLICK_LIVE_TOKEN as CLICK_TOKEN, PAY_COM_LIVE_TOKEN as PAYME_TOKEN

def get_price_label(label: str, amount: int):
    PRICE = LabeledPrice(label=label, amount=amount*100)
    return PRICE

async def on_callback_query(callback_query: CallbackQuery):
    await callback_query.answer()  # Yaqin kelgan so'rovni qabul qilish

    if callback_query.data.startswith("click_"):
        book_id = callback_query.data.replace("click_", "")
        book_name = get_premium_book_name(book_id)
        await bot.send_invoice(
                callback_query.from_user.id,
                title=f"{book_name}",
                description=f"Click orqali to'lov",
                provider_token=CLICK_TOKEN,  # Click taminotchisining tokeni
                currency="uzs",
                is_flexible=False,
                prices=[get_price_label(f"{book_name}", int(get_premium_book_price(name=book_name)))],
                start_parameter="premium-book-subcription",
                payload=book_name,
            )
    elif callback_query.data.startswith("payme_"):
        book_id = callback_query.data.replace("payme_", "")
        book_name = get_premium_book_name(book_id)
        await bot.send_invoice(
                callback_query.from_user.id,
                title=f"{book_name}",
                description=f"Payme orqali to'lov",
                provider_token=PAYME_TOKEN,  # Click taminotchisining tokeni
                currency="uzs",
                is_flexible=False,
                prices=[get_price_label(f"{book_name}", int(get_premium_book_price(name=book_name)))],
                start_parameter="premium-book-subcription",
                payload=book_name,
            )

from aiogram.types import LabeledPrice, CallbackQuery

from loader import bot
from database.database import get_premium_book_name_by_id, get_premium_book_description_by_id, get_premium_book_price_by_id, get_premium_audiobook_price_by_id
from config import PAY_CLICK_LIVE_TOKEN as CLICK_TOKEN, PAY_COM_LIVE_TOKEN as PAYME_TOKEN

def get_price_label(label: str, amount: int):
    PRICE = LabeledPrice(label=label, amount=amount*100)
    return PRICE

async def on_callback_query(callback_query: CallbackQuery):
    await callback_query.answer()  # Yaqin kelgan so'rovni qabul qilish
    if callback_query.data.startswith("click_"):
        book_id = callback_query.data.split("_")[1]
        book_name = get_premium_book_name_by_id(book_id)
        if callback_query.data.split('_')[-1] == "e":
            await bot.send_invoice(
                    callback_query.from_user.id,
                    title=f"{book_name}",
                    description=f"Click orqali to'lov",
                    provider_token=CLICK_TOKEN,  # Click taminotchisining tokeni
                    currency="uzs",
                    is_flexible=False,
                    prices=[get_price_label(f"{book_name}", int(get_premium_book_price_by_id(book_id)))],
                    start_parameter="premium-book-subcription",
                    payload=f"{book_name}_{callback_query.data.split('_')[-1]}",
                )
        elif callback_query.data.split('_')[-1] == "a":
                await bot.send_invoice(
                    callback_query.from_user.id,
                    title=f"{book_name}",
                    description=f"Click orqali to'lov",
                    provider_token=CLICK_TOKEN,  # Click taminotchisining tokeni
                    currency="uzs",
                    is_flexible=False,
                    prices=[get_price_label(f"{book_name}", int(get_premium_audiobook_price_by_id(book_id)))],
                    start_parameter="premium-book-subcription",
                    payload=f"{book_name}_{callback_query.data.split('_')[-1]}",
                )
            
    elif callback_query.data.startswith("payme_"):
        book_id = callback_query.data.split("_")[1]
        book_name = get_premium_book_name_by_id(book_id)
        if callback_query.data.split('_')[-1] == "e":
            await bot.send_invoice(
                    callback_query.from_user.id,
                    title=f"{book_name}",
                    description=f"Payme orqali to'lov",
                    provider_token=PAYME_TOKEN,  # Payme taminotchisining tokeni
                    currency="uzs",
                    is_flexible=False,
                    prices=[get_price_label(f"{book_name}", int(get_premium_book_price_by_id(book_id)))],
                    start_parameter="premium-book-subcription",
                    payload=f"{book_name}_{callback_query.data.split('_')[-1]}",
                )
        elif callback_query.data.split('_')[-1] == "a":
                await bot.send_invoice(
                    callback_query.from_user.id,
                    title=f"{book_name}",
                    description=f"Payme orqali to'lov",
                    provider_token=PAYME_TOKEN,  # Payme taminotchisining tokeni
                    currency="uzs",
                    is_flexible=False,
                    prices=[get_price_label(f"{book_name}", int(get_premium_audiobook_price_by_id(book_id)))],
                    start_parameter="premium-book-subcription",
                    payload=f"{book_name}_{callback_query.data.split('_')[-1]}",
                )
                
    elif callback_query.data.startswith("visa_"):
        book_id = callback_query.data.split("_")[1]
        book_name = get_premium_book_name_by_id(book_id)
        if callback_query.data.split('_')[-1] == "e":
            tes = f"Agar toʻlov tizimida muammoga duch kelgan boʻlsangiz, unda quyidagi tartibda toʻlovni amalga oshirishingiz mumkin. Quyidagi kartalarga 👇\n\nVisa: 4231 2000 0823 7124\n\nUzcard: 5614 6810 1706 4589\n(Muzaffarjon Ne’matov)\n\nToʻlovni amalga oshirib ushbu @narrator_uz akkauntiga toʻlov kvitansiyasini va qaysi kitobni tanlaganingizni yuborasiz. Soʻngra sizning chekingiz tekshirilib audiokitoblar guruhiga qabul qilinasiz.\n\n💰Asar narxi - {book_id} soʻm"
            await bot.send_message(callback_query.from_user.id, tes)
        elif callback_query.data.split('_')[-1] == "a":
            tes = f"Agar toʻlov tizimida muammoga duch kelgan boʻlsangiz, unda quyidagi tartibda toʻlovni amalga oshirishingiz mumkin. Quyidagi kartalarga 👇\n\nVisa: 4231 2000 0823 7124\n\nUzcard: 5614 6810 1706 4589\n(Muzaffarjon Ne’matov)\n\nToʻlovni amalga oshirib ushbu @narrator_uz akkauntiga toʻlov kvitansiyasini va qaysi kitobni tanlaganingizni yuborasiz. Soʻngra sizning chekingiz tekshirilib audiokitoblar guruhiga qabul qilinasiz.\n\n💰Audiokitob narxi - {get_premium_audiobook_price_by_id(book_id)} soʻm"
            await bot.send_message(callback_query.from_user.id, tes)            

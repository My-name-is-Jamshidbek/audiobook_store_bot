from aiogram.types import CallbackQuery, Message as m
from aiogram import executor
from datetime import datetime

from loader import pay_bot, pay_dp, bot
from database.database import get_buy_uc_tg_id, update_thrown_away_status
from buttons.inlinekeyboardbuttons import create_inline_keyboard
from config import ADMIN_ID

async def on_shutdown(dp):
    text = f"""
            Salom admin.
bot ishdan toxtadi!
server vaqti: {datetime.now()}
        """
    await pay_bot.send_message(ADMIN_ID, text)
    await pay_bot.close()
    print("Bot ishdan to'xtadi: " + str(datetime.now()))


async def on_startup(dp):
    text = f"""
            Salom admin.
bot ishga tushdi!
server vaqti: {datetime.now()}
        """
    await pay_bot.send_message(ADMIN_ID,text)
    print("Bot ishga tushdi: "+str(datetime.now()))


@pay_dp.callback_query_handler()
async def buy_or_close(call: CallbackQuery):
    _m = call.data
    await call.answer()  # Yaqin kelgan so'rovni qabul qilish
    if _m.split("_")[0] == "check":
        update_thrown_away_status(_m.split("_")[1])
        _tgid = get_buy_uc_tg_id(_m.split("_")[1])
        await bot.send_message(_tgid, f"Sizning {_m.split('_')[1]} raqamli haridigiz amalga oshirildi ✅")        
        await call.message.delete()
        await pay_bot.send_message(ADMIN_ID, f"AMALGA OSHIRILGAN BUYURTMA\nid: {_m.split('_')[1]}")
        # await pay_bot.edit_message_reply_markup(ADMIN_ID, call.message.delete(), reply_markup=create_inline_keyboard([{"text": "TO'LANGAN", "data": "payed"}]))
    elif _m.split("_")[0] == "close":
        _tgid = get_buy_uc_tg_id(_m.split("_")[1])
        await bot.send_message(_tgid, f"Sizning {_m.split('_')[1]} raqamli haridingizda muammo kelib chiqdi ❌ Qaytadan urinib ko’rig yoki  <a href=\"https://t.me/vooALISHER\">Admin</a>ga murojat qilig 🤵🏻")        
        await pay_bot.send_message(ADMIN_ID, f"BEKOR QILINGAN BUYURTMA\nid: {_m.split('_')[1]}")
        await call.message.delete()
        # await pay_bot.edit_message_reply_markup(ADMIN_ID, call.message.from_id, reply_markup=create_inline_keyboard([{"text": "BEKOR QILINGAN", "data": "closed"}]))
@pay_dp.message_handler()
async def start(m: m):
    await m.answer("Bot ishga tayyor!")

if __name__=='__main__':
    executor.start_polling(pay_dp,on_startup=on_startup,on_shutdown=on_shutdown)

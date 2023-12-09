"""
admin apps
"""
import os
import uuid

from aiogram.types import Message as m, InputFile
from aiogram.dispatcher import FSMContext as s

from buttons.keyboardbuttons import keyboardbutton
from buttons.inlinekeyboardbuttons import get_group_link_button
from database.database import *
from loader import bot
from states import *
from config import main_menu_list

async def check_join(chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member["status"] != "left"
    except Exception as e:
        print(e)
        return False
    
    
async def admin_main_menu(m: m, state: s):
    if m.text == "Biz bilan aloqa 📞":
        await state.update_data(change=1)
        await m.answer(get_latest_contact_message(), reply_markup=keyboardbutton(["O'zgartirish", "Chiqish"]))
        await Admin_state.contact_us.set()
    elif m.text == "Statistika 📊":
        await m.answer(f"Foydalanuvchilar statistikasi:\nJami: {count_starters_users()} nafar\nRo'yxatdan o'tgan: {all_users_count()} nafar")
    elif m.text == "UC Chiqarish":
        await state.update_data(change=2)
        await m.answer(f"UC chiqarishning minimal miqdori {get_setting('min_release_uc')} uc ga teng", reply_markup=keyboardbutton(["O'zgartirish", "Chiqish"]))
        await Admin_state.contact_us.set()
    elif m.text == "Odam qo'shish":
        await state.update_data(change=3)
        await m.answer(f"Har bir taklif qilingan foydalanuvchi uchun beriladigan uc {get_setting('add_man_uc')} uc ga teng", reply_markup=keyboardbutton(["O'zgartirish", "Chiqish"]))
        await Admin_state.contact_us.set()
    elif m.text == "Boshlang'ich uc":
        await state.update_data(change=4)
        await m.answer(f"Yangi foydalanuvchilardagi boshlang'ich uc miqdori {get_setting('starter_uc')}", reply_markup=keyboardbutton(["O'zgartirish", "Chiqish"]))
        await Admin_state.contact_us.set()
    elif m.text == "Reklama":
        await m.answer("Reklama habarini yuboring:", reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.ad_message.set()
    elif m.text == "Kanallar":
        await m.answer("Foydalanuvchi ro'yxatdan o'tishi uchun a'zo bo'lishi kerak bo'lgan kanallar ro'yxati:", reply_markup=keyboardbutton(get_channels_names()+["Chiqish", "Qo'shish"]))
        await Admin_state.change_group.set()
    elif m.text == "UC narxlar":
        data = get_uc_prices()
        f = ""
        for i in data:f+=f"\n{i[0]}. {i[1]} so'm {int(i[2])} uc"
        await m.answer("UC narxlari:"+f, reply_markup=keyboardbutton(["O'chirish", "Qo'shish", "Chiqish"]))
        await Admin_state.uc_prices.set()
    elif m.text == "Foydalanuvchi":
        await m.answer("Foydalanuchining telegram idsini kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.get_user.set()
    elif m.text == "To'lov ma'lumoti":
        await state.update_data(change=5)
        await m.answer(f"{get_setting('payment_message')}", reply_markup=keyboardbutton(["O'zgartirish", "Chiqish"]))
        await Admin_state.contact_us.set()


async def admin_get_user(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    elif user_exists(m.text):
        tg_id = m.text
        try: 
            fullname = get_fullname_user_by_tg_id(tg_id)
        except:
            fullname = "Aniqlanmadi"
        try:
            uc_amount = get_uc(tg_id)
        except:
            uc_amount = "Aniqlanmadi"
        try:
            invited_people = get_invite(tg_id)
        except:
            invited_people = "Aniqlanmadi"
        f = f"Foydalanuvchi malumotlari:\n\nTO'LIQ ISMI: {fullname}\nHISOB: {uc_amount}\nTAKLIFLAR: {invited_people}"
        await m.answer(f)
    else:
        await m.answer("Foydalanuvchi topilmadi!")

async def admin_uc_prices(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    elif m.text == "O'chirish":
        btns = [f"{i[0]}" for i in get_uc_prices()]
        await m.answer("O'chirmoqchi bo'lgan qatoringizni tanlang:", reply_markup=keyboardbutton(btns+["Chiqish"], row=3))
        await Admin_state.uc_del.set()
    elif m.text == "Qo'shish":
        await m.answer("UC miqdorini kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.uc_add_amount.set()


async def Admin_uc_del(m: m, state: s):
    btns = [f"{i[0]}" for i in get_uc_prices()]
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    elif m.text in btns:
        delete_uc_price_by_id(m.text)
        await m.answer("O'chirildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    


async def admin_add_uc_amount(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    elif m.text:
        await m.answer("Narxni kiriting:")
        await state.update_data(amount=m.text)
        await Admin_state.uc_add_price.set()


async def admin_add_uc_price(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    elif m.text:
        data = await state.get_data()
        add_uc_price(price=m.text, amount=data.get("amount"))
        await m.answer("Muvaffaqiyatli qo'shildi", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    

async def admin_change_group(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    elif m.text in get_channels_names():
        await state.update_data(changed_group = m.text)
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["O'chirish", "Chiqish"]))    
        await Admin_state.changed_group.set()
    elif m.text == "Qo'shish":
        await m.answer("Yangi kanal nomini kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.add_group_name.set()

async def admin_add_group_name(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Foydalanuvchi ro'yxatdan o'tishi uchun a'zo bo'lishi kerak bo'lgan kanallar ro'yxati:", reply_markup=keyboardbutton(get_channels_names()+["Chiqish", "Qo'shish"]))
        await Admin_state.change_group.set()
    elif m.text in get_channels_names():
        await m.answer("Bu nomli kanal mavjud iltimos boshqa nom kiriting!")    
    else:
        await state.update_data(add_channel_name=m.text)
        await m.answer("Botni kanalga qo'shib to'liq adminlikni bering va kanal linkini tashlang:\nNamuna: @kanallinki")
        await Admin_state.add_channel_link.set()

async def admin_add_channel_link(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Foydalanuvchi ro'yxatdan o'tishi uchun a'zo bo'lishi kerak bo'lgan kanallar ro'yxati:", reply_markup=keyboardbutton(get_channels_names()+["Chiqish", "Qo'shish"]))
        await Admin_state.change_group.set()
    elif await check_join(chat_id=m.text, user_id=str(m.from_user.id)):
        data = await state.get_data()
        add_channel(data.get("add_channel_name"), m.text)
        await m.answer("Kanal muvaffaqiyatli qo'shildi!")
        await m.answer("Foydalanuvchi ro'yxatdan o'tishi uchun a'zo bo'lishi kerak bo'lgan kanallar ro'yxati:", reply_markup=keyboardbutton(get_channels_names()+["Chiqish", "Qo'shish"]))
        await Admin_state.change_group.set()
    else:
        await m.answer("Iltimos kanal linkini, bot to'liq adminligini va o'zingiz kanalga qo'shilganligingizni tekshiring va linkni qayta jo'nating:")        

async def admin_changed_group(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Foydalanuvchi ro'yxatdan o'tishi uchun a'zo bo'lishi kerak bo'lgan kanallar ro'yxati:", reply_markup=keyboardbutton(get_channels_names()+["Chiqish", "Qo'shish"]))
        await Admin_state.change_group.set()
    elif m.text == "O'chirish":
        data = await state.get_data()
        delete_channel(data.get("changed_group"))
        await m.answer("Kanal muvaffaqiyatli o'chirildi!")
        await m.answer("Foydalanuvchi ro'yxatdan o'tishi uchun a'zo bo'lishi kerak bo'lgan kanallar ro'yxati:", reply_markup=keyboardbutton(get_channels_names()+["Chiqish", "Qo'shish"]))
        await Admin_state.change_group.set()

            
async def Admin_ad_message(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    else:
        m_id = m.message_id
        await m.answer("Reklama taqdim etilishi kerak bo'lgan foydalanuvchilarni tanlang:", reply_markup=keyboardbutton(["Barcha foydalanuvchilarga", "Ro'yxatdan o'tganlarga", "Chiqish"]))
        await state.update_data(ad_m_id=m_id)
        await Admin_state.ad_users_type.set()


async def send_ad(A_ID, m_id, users):
    c, e = 0,0
    _id = await bot.send_message(A_ID, f"Reklama jo'natilmoqda jami {len(users)} nafar")
    for i in users:
        try:
            await bot.forward_message(i, A_ID, m_id,)
            c+=1
        except:
            e+=1
    await _id.delete()
    await bot.send_message(A_ID, f"Reklama jo'natildi\nMuvaffaqiyatli {c}\nMuvaffaqiyatsiz: {e}", reply_to_message_id=m_id)

async def Admin_ad_message_type(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    else:
        data = await state.get_data()
        m_id = data.get("ad_m_id")
        A_ID = m.from_user.id
        if m.text == "Barcha foydalanuvchilarga":
            users = get_all_starters_tg_id() 
        elif m.text == "Ro'yxatdan o'tganlarga":
            users = get_all_users_tg_id()
        users = list(set(list(map(int, users))))
        await send_ad(A_ID=A_ID, m_id=m_id, users=users)
        await m.answer("Asosiy menyu", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()


async def admin_contact_us(m: m, state: s):
    if m.text=="O'zgartirish":
        data = await state.get_data()
        change = data.get("change")
        if int(change)==1:await m.answer("Yangi habarni yuboring:", reply_markup=keyboardbutton(["Chiqish"]))
        elif int(change)==2:await m.answer("Yangi minimal uc chiqarish miqdorini kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        elif int(change)==3:await m.answer("Yangi odam qo'shishuchun beriladigan uc miqdorini kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        elif int(change)==4:await m.answer("Yangi foydalanuvchilarga beriladigan uc miqdorini kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        elif int(change)==5:await m.answer("Yangi foydalanuvchilarning to'lov ma'lumotini kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.contact_us_change.set()
    elif m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()


async def admin_contact_us_change(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()
    elif m.text:
        data = await state.get_data()
        change = data.get("change")
        if int(change)==1:insert_contact_message(m.text)
        elif int(change)==2:update_setting("min_release_uc", m.text)
        elif int(change)==3:update_setting("add_man_uc", m.text)
        elif int(change)==4:update_setting("starter_uc", m.text)
        elif int(change)==5:update_setting("payment_message", m.text)
        await m.answer("Yangilandi!", reply_markup=keyboardbutton(main_menu_list, row=2))
        await Admin_state.main_menu.set()


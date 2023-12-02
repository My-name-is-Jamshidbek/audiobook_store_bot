from database.database import *

top_users = get_maximum_amount_users(limit=5)

for user in top_users:
    user_id, max_amount = user
    user_name = get_user_name_by_id(user_id)
    print(f"Foydalanuvchi ID: {user_id}, Foydalanuvchi nomi: {user_name}, Maksimum miqdori: {max_amount}")
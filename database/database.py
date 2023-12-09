from database.database_additional import *
from database.database_additional1 import *

def create_database():
    create_contact_table()
    create_user_table()
    create_starters_table()
    create_invite_table()
    create_uc_table()
    create_settings_table()
    # add_setting("min_release_uc", "5")
    # add_setting("add_man_uc", "1")
    # add_setting("starter_uc", "5")
    create_channels_table()
    create_uc_price_table()
    create_buy_uc_table()

from aiogram.types import LabeledPrice

def get_price_label(label: str, amount: int):
    PRICE = LabeledPrice(label=label, amount=amount*100)
    return PRICE

import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command

API_TOKEN = "8330667955:AAE7vRKA5_W-GqgVQHiKWfspCvDcPqZCDhA"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_active = {}
user_ids = {}

# Apple grid tayyorlash
def make_grid(ap):
    rows = len(ap)
    cols = len(ap[0])
    out = ""
    for r in reversed(range(rows)):
        for c in range(cols):
            out += "🍏" if ap[r][c] == 1 else "🍎"
        out += "\n"
    return out

# --- /start handler ---
@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    uid = msg.from_user.id
    user_active[uid] = True
    user_ids[uid] = None

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="1xBet")]],
        resize_keyboard=True
    )
    await msg.answer(f"Hello {msg.from_user.first_name}! You are Welcome ⚡", reply_markup=kb)

# --- 1xBet bosilganda ID so‘rash ---
@dp.message()
async def handle_1xbet(msg: types.Message):
    uid = msg.from_user.id
    text = msg.text

    if not user_active.get(uid):
        return await msg.answer("You are not activated")

    if text == "1xBet":
        await msg.answer("Please send your ID:")
        return

    if text.isdigit():
        user_ids[uid] = text
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="GET SIGNAL")]],
            resize_keyboard=True
        )
        await msg.answer("ID saved! Now press GET SIGNAL", reply_markup=kb)
        return

    if text in ["GET SIGNAL", "REFRESH SIGNAL"]:
        if not user_ids.get(uid):
            return await msg.answer("Please send your ID first")

        data = {
            "user_id": user_ids[uid],
            "otp_code": "BYTROX-VIP-3RYICW-MNA21N-07Y",
            "key": "ran"
        }

        try:
            r = requests.post("https://bytrox.shop/apple/specialdata.php", json=data, timeout=10)
            js = r.json()
        except Exception:
            return await msg.answer("Invalid")

        if "AP" not in js:
            return await msg.answer("Invalid")

        ap = js["AP"]
        grid = make_grid(ap)

        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="REFRESH SIGNAL")]],
            resize_keyboard=True
        )
        await msg.answer(f"{grid}\nSignal refreshed ✅", reply_markup=kb)
        return

    await msg.answer("Invalid command.")

# --- Bot ishga tushurish ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

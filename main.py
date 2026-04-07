import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# =========================
# НАСТРОЙКИ
# =========================
TOKEN = "8764484233:AAH4ugVnM6N66fS4ywCpdQ9VUNhihYvIjiA"
SELLER_USERNAME = "GGDONAT1"

# =========================
# ТОВАРЫ
# =========================
PRODUCTS = {
    "⭐ Telegram Stars": {
        "100 ⭐": "30 000 сум",
        "150 ⭐": "45 000 сум",
        "250 ⭐": "70 000 сум",
        "350 ⭐": "95 000 сум",
        "500 ⭐": "140 000 сум",
        "750 ⭐": "199 000 сум",
        "1000 ⭐": "285 000 сум",
    },

    "💎 FC Points": {
        "40 + 40": "13 000 сум",
        "100 + 100": "25 000 сум",
        "500 + 500": "96 000 сум",
        "1000 + 1000": "195 000 сум",
        "2000 + 2000": "380 000 сум",
    },

    "🌟 Звёздный абонемент": {
        "Абонемент": "195 000 сум",
        "+20 уровней": "370 000 сум",
    },

    "🔥 Brawl Pass": {
        "Brawl Pass": "70 000 сум",
        "Brawl Pass Plus": "110 000 сум",
    },

    "💎 Гемы": {
        "30 гемов": "16 000 сум",
        "80 гемов": "40 000 сум",
        "170 гемов": "74 000 сум",
        "360 гемов": "145 000 сум",
        "950 гемов": "355 000 сум",
        "2000 гемов": "685 000 сум",
    },

    "⭐ Telegram Premium": {
        "На 1 месяц": "60 000 сум",
        "На 1 год (каждый месяц по 40 000 сум)": "40 000 сум",
    },

    "📝 Отзывы": {
        "Посмотреть отзывы": "Нажми и смотри",
    }
}

# =========================
# ОПИСАНИЯ КАТЕГОРИЙ
# =========================
CATEGORY_INFO = {
    "⭐ Telegram Stars": """⭐ TELEGRAM STARS — ВЫГОДНО И БЫСТРО ⭐

🚀 Пополняй звёзды без лишних переплат
🔒 Надёжно | Проверено

💰 Цены:
• 100 ⭐ — 30 000 сум
• 150 ⭐ — 45 000 сум
• 250 ⭐ — 70 000 сум
• 350 ⭐ — 95 000 сум
• 500 ⭐ — 140 000 сум
• 750 ⭐ — 199 000 сум
• 1000 ⭐ — 285 000 сум

🔥 Успей купить по текущим ценам

📩 Заказ: @GGDONAT1""",

    "💎 FC Points": """💎 FC POINTS — ЗАЛЕТАЙ ПО ВЫГОДЕ 💎

🚀 Хочешь топ состав и быстрый апгрейд?
Не трать время — бери FC Points с бонусом x2!

🔥 Только сейчас:
✔️ Двойной бонус к каждому паку
✔️ Моментальная выдача
✔️ Проверенный продавец

💰 Цены:
• 40 + 40 — 13 000 сум
• 100 + 100 — 25 000 сум
• 500 + 500 — 96 000 сум
• 1000 + 1000 — 195 000 сум
• 2000 + 2000 — 380 000 сум

⚡ Успей купить по этим ценам — потом будет дороже

📩 Пиши прямо сейчас: @GGDONAT1""",

    "🌟 Звёздный абонемент": """🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ 🌟

🔥 Легендарный 120 KLOSE уже доступен!
Прокачай состав и забери топ игрока прямо сейчас ⚽💥

💰 Цены:
⭐ Абонемент — 195 000 сум
🚀 +20 уровней — 370 000 сум

✨ Что получаешь:
✔️ Топовый игрок 120 OVR
✔️ Кучу наград и ресурсов
✔️ Быстрый прогресс
✔️ Максимум буста для аккаунта

📩 Заказ: @GGDONAT1
⚡ Быстро | Надежно | Безопасно

Не упусти шанс забрать имбу в свой состав 🔥""",

    "🔥 Brawl Pass": """🔥 BRAWL PASS АКЦИЯ 🔥

Прокачай свой аккаунт в Brawl Stars на максимум 🚀

💰 Цены:
🎟️ Brawl Pass — 70 000 сум
🎟️ Brawl Pass Plus — 110 000 сум 💎

✨ Что получаешь:
✔️ Эксклюзивные награды
✔️ Быстрый прогресс
✔️ Больше ресурсов и ключей
✔️ Дополнительные бонусы в Plus

📩 Заказ: @GGDONAT1
⚡ Быстро | Надежно | Безопасно

Не упусти шанс забрать топ-награды 🔥""",

    "💎 Гемы": """💎 ГЕМЫ В НАЛИЧИИ 💎

🚀 Быстрое пополнение | Надежно | Без лишних заморочек

💰 Цены:
🔹 30 гемов — 16 000 сум
🔹 80 гемов — 40 000 сум
🔹 170 гемов — 74 000 сум
🔹 360 гемов — 145 000 сум
🔹 950 гемов — 355 000 сум 🔥
🔹 2000 гемов — 685 000 сум 💎

✨ Почему мы?
✔️ Моментальная выдача
✔️ Выгодные цены
✔️ Проверенный сервис

📩 Заказ: @GGDONAT1
⚡ Успей прокачать свой аккаунт уже сейчас!""",

    "⭐ Telegram Premium": """⭐ Telegram Premium ⭐

🚀 Открой больше возможностей в Telegram!
Эксклюзивные функции, высокая скорость и максимум комфорта 💎

💰 Тарифы:
📅 На 1 месяц — 60 000 сум
📆 На 1 год — 40 000 сум / месяц 🔥

✨ Что получаешь:
✔️ Быстрая загрузка файлов
✔️ Увеличенные лимиты
✔️ Уникальные стикеры и реакции
✔️ Отключение рекламы
✔️ И многое другое!

📩 Заказать: @GGDONAT1
⚡ Быстро | Надежно | Доступно

Не упусти шанс прокачать свой Telegram 💜""",

    "📝 Отзывы": """📝 ОТЗЫВЫ НАШИХ ПОКУПАТЕЛЕЙ

⭐ Тут ты можешь посмотреть отзывы перед покупкой.

🔥 Почему нам доверяют:
✔️ Быстрая выдача
✔️ Честные цены
✔️ Постоянные клиенты
✔️ Надёжность

📩 Если тоже хочешь заказать:
@GGDONAT1

👇 Нажми кнопку ниже, чтобы посмотреть отзывы."""
}

# =========================
# ССЫЛКА НА ОТЗЫВЫ
# =========================
REVIEWS_LINK = "https://t.me/uzdinat2"


# =========================
# КНОПКИ
# =========================
def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="⭐ Telegram Stars", callback_data="cat:⭐ Telegram Stars")
    kb.button(text="💎 FC Points", callback_data="cat:💎 FC Points")
    kb.button(text="🌟 Звёздный абонемент", callback_data="cat:🌟 Звёздный абонемент")
    kb.button(text="🔥 Brawl Pass", callback_data="cat:🔥 Brawl Pass")
    kb.button(text="💎 Гемы", callback_data="cat:💎 Гемы")
    kb.button(text="⭐ Telegram Premium", callback_data="cat:⭐ Telegram Premium")
    kb.button(text="📝 Отзывы", callback_data="cat:📝 Отзывы")
    kb.adjust(1)
    return kb.as_markup()


def category_menu(category_name: str):
    kb = InlineKeyboardBuilder()

    if category_name == "📝 Отзывы":
        kb.button(text="📝 Смотреть отзывы", url=REVIEWS_LINK)
        kb.button(text="📩 Связаться с продавцом", url=f"https://t.me/{SELLER_USERNAME}")
        kb.button(text="⬅️ Назад", callback_data="back_main")
        kb.adjust(1)
        return kb.as_markup()

    items = PRODUCTS.get(category_name, {})
    for item_name, price in items.items():
        kb.button(
            text=f"{item_name} — {price}",
            callback_data=f"buy:{category_name}:{item_name}"
        )

    kb.button(text="📩 Связаться с продавцом", url=f"https://t.me/{SELLER_USERNAME}")
    kb.button(text="⬅️ Назад", callback_data="back_main")
    kb.adjust(1)
    return kb.as_markup()


def back_to_category(category_name: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data=f"cat:{category_name}")
    kb.button(text="🏠 Главное меню", callback_data="back_main")
    kb.adjust(1)
    return kb.as_markup()


# =========================
# БОТ
# =========================
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    text = """🔥 Добро пожаловать в магазин доната 🔥

Здесь ты можешь быстро и удобно купить:
⭐ Telegram Stars
💎 FC Points
🌟 Звёздный абонемент
🔥 Brawl Pass
💎 Гемы
⭐ Telegram Premium

🛒 Выбирай нужный товар ниже 👇"""
    await message.answer(text, reply_markup=main_menu())


@dp.callback_query(F.data.startswith("cat:"))
async def category_handler(callback: CallbackQuery):
    category_name = callback.data.split("cat:")[1]
    text = CATEGORY_INFO.get(category_name, "Категория не найдена.")
    await callback.message.edit_text(text, reply_markup=category_menu(category_name))
    await callback.answer()


@dp.callback_query(F.data == "back_main")
async def back_main_handler(callback: CallbackQuery):
    text = """🔥 Добро пожаловать в магазин доната 🔥

Здесь ты можешь быстро и удобно купить:
⭐ Telegram Stars
💎 FC Points
🌟 Звёздный абонемент
🔥 Brawl Pass
💎 Гемы
⭐ Telegram Premium

🛒 Выбирай нужный товар ниже 👇"""
    await callback.message.edit_text(text, reply_markup=main_menu())
    await callback.answer()


@dp.callback_query(F.data.startswith("buy:"))
async def buy_handler(callback: CallbackQuery):
    _, category_name, item_name = callback.data.split(":", 2)
    price = PRODUCTS[category_name][item_name]

    text = f"""✅ Вы выбрали:

📦 Товар: {item_name}
💰 Цена: {price}
📂 Категория: {category_name}

📩 Для заказа напишите продавцу:
@{SELLER_USERNAME}

⚡ После оплаты отправьте:
• Скрин оплаты
• Что именно хотите купить
• Ваш Telegram / данные для заказа
"""

    kb = InlineKeyboardBuilder()
    kb.button(text="📩 Написать продавцу", url=f"https://t.me/{SELLER_USERNAME}")
    kb.button(text="⬅️ Назад", callback_data=f"cat:{category_name}")
    kb.button(text="🏠 Главное меню", callback_data="back_main")
    kb.adjust(1)

    await callback.message.edit_text(text, reply_markup=kb.as_markup())
    await callback.answer()


# =========================
# ЗАПУСК
# =========================
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

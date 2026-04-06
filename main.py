import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------------- НАСТРОЙКИ ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

PAYMENT_TEXT = """
💳 Оплата:

Номер карты Click:
5614680504235934

Номер карты Payme:
5614680504235934

👤 Получатель:
ARTIKOVA ZUXRA

📱 Номер телефона:
93 597 27 47

🏧 Можно оплатить через банкомат

❌ На номер НЕ кидать
🛑 За ошибочный перевод не ручаюсь

После оплаты нажмите:
✅ Я оплатил
"""

# ---------------- ТОВАРЫ ----------------
PRODUCTS = {
    "⭐ TELEGRAM STARS": {
        "100 ⭐": "30 000 сум",
        "150 ⭐": "45 000 сум",
        "250 ⭐": "70 000 сум",
        "350 ⭐": "95 000 сум",
        "500 ⭐": "140 000 сум",
        "750 ⭐": "199 000 сум",
        "1000 ⭐": "285 000 сум",
    },
    "💎 FC POINTS": {
        "40 + 40": "13 000 сум",
        "100 + 100": "25 000 сум",
        "500 + 500": "96 000 сум",
        "1000 + 1000": "195 000 сум",
        "2000 + 2000": "380 000 сум",
    },
    "🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ": {
        "Абонемент": "195 000 сум",
        "+20 уровней": "370 000 сум",
    },
    "🔥 BRAWL PASS": {
        "Brawl Pass": "70 000 сум",
        "Brawl Pass Plus": "110 000 сум",
    },
    "💎 ГЕМЫ": {
        "30 гемов": "16 000 сум",
        "80 гемов": "40 000 сум",
        "170 гемов": "74 000 сум",
        "360 гемов": "145 000 сум",
        "950 гемов": "355 000 сум",
        "2000 гемов": "685 000 сум",
    },
    "⭐ Telegram Premium": {
    "На 1 месяц": "60 000 сум",
    "На год (каждый месяц по 40 000 сум)": "480 000 сум"
    }
    },
}

CATEGORY_INFO = {
    "⭐ TELEGRAM STARS": """⭐ TELEGRAM STARS — ВЫГОДНО И БЫСТРО ⭐

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

🔥 Успей купить по текущим ценам""",

    "💎 FC POINTS": """💎 FC POINTS — ЗАЛЕТАЙ ПО ВЫГОДЕ 💎

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

⚡ Успей купить по этим ценам — потом будет дороже""",

    "🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ": """🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ 🌟

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

⚡ Быстро | Надежно | Безопасно""",

    "🔥 BRAWL PASS": """🔥 BRAWL PASS АКЦИЯ 🔥

Прокачай свой аккаунт в Brawl Stars на максимум 🚀

💰 Цены:
🎟️ Brawl Pass — 70 000 сум
🎟️ Brawl Pass Plus — 110 000 сум

✨ Что получаешь:
✔️ Эксклюзивные награды
✔️ Быстрый прогресс
✔️ Больше ресурсов и ключей
✔️ Дополнительные бонусы в Plus

⚡ Быстро | Надежно | Безопасно""",

    "💎 ГЕМЫ": """💎 ГЕМЫ В НАЛИЧИИ 💎

🚀 Быстрое пополнение | Надежно | Без лишних заморочек

💰 Цены:
🔹 30 гемов — 16 000 сум
🔹 80 гемов — 40 000 сум
🔹 170 гемов — 74 000 сум
🔹 360 гемов — 145 000 сум
🔹 950 гемов — 355 000 сум
🔹 2000 гемов — 685 000 сум

✨ Почему мы?
✔️ Моментальная выдача
✔️ Выгодные цены
✔️ Проверенный сервис""",

    "⭐ Telegram Premium": """⭐ Telegram Premium ⭐

🚀 Открой больше возможностей в Telegram!
Эксклюзивные функции, высокая скорость и максимум комфорта 💎

💰 Тарифы:
📅 На 1 месяц — 60 000 сум
📆 На год — 40 000 сум каждый месяц 

✨ Что получаешь:
✔️ Быстрая загрузка файлов
✔️ Увеличенные лимиты
✔️ Уникальные стикеры и реакции
✔️ Отключение рекламы
✔️ И многое другое!

⚡ Быстро | Надежно | Доступно"""
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---------------- КНОПКИ ----------------
def main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🛒 Купить"), KeyboardButton("💰 Прайс")],
            [KeyboardButton("🎁 Акции"), KeyboardButton("📦 Мои заказы")],
            [KeyboardButton("⭐ Отзывы"), KeyboardButton("🛠 Поддержка")],
            [KeyboardButton("📋 Что есть у нас")],
        ],
        resize_keyboard=True
    )

def category_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("⭐ TELEGRAM STARS")],
            [KeyboardButton("💎 FC POINTS")],
            [KeyboardButton("🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ")],
            [KeyboardButton("🔥 BRAWL PASS")],
            [KeyboardButton("💎 ГЕМЫ")],
            [KeyboardButton("⭐ Telegram Premium")],
            [KeyboardButton("⬅️ Назад")],
        ],
        resize_keyboard=True
    )

def products_menu(category):
    buttons = []
    for item in PRODUCTS[category]:
        buttons.append([KeyboardButton(item)])
    buttons.append([KeyboardButton("⬅️ Назад")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def payment_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("✅ Я оплатил")],
            [KeyboardButton("⬅️ Назад")],
        ],
        resize_keyboard=True
    )

# ---------------- СТАРТ ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в магазин 🔥

Выберите нужный раздел ниже 👇
"""
    await update.message.reply_text(text, reply_markup=main_menu())

# ---------------- ТЕКСТ ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "/start":
        await start(update, context)
        return

    if text == "🛒 Купить":
        await update.message.reply_text(
            "Выберите категорию товара 👇",
            reply_markup=category_menu()
        )
        return

    if text == "💰 Прайс":
        msg = "💰 НАШ ПРАЙС:\n\n"
        for category, items in PRODUCTS.items():
            msg += f"{category}\n"
            for name, price in items.items():
                msg += f"• {name} — {price}\n"
            msg += "\n"
        await update.message.reply_text(msg, reply_markup=main_menu())
        return

    if text == "🎁 Акции":
        await update.message.reply_text(
            "🎁 Актуальные акции уже указаны в категориях товаров.",
            reply_markup=main_menu()
        )
        return

    if text == "📦 Мои заказы":
        await update.message.reply_text(
            "📦 Ваши заказы пока не сохраняются в истории.\n\nПосле оплаты админ получает заявку.",
            reply_markup=main_menu()
        )
        return

    if text == "⭐ Отзывы":
        await update.message.reply_text(
            "⭐ Отзывы можно добавить позже отдельным разделом.",
            reply_markup=main_menu()
        )
        return

    if text == "🛠 Поддержка":
        await update.message.reply_text(
            "🛠 Поддержка: @GGDONAT1",
            reply_markup=main_menu()
        )
        return

    if text == "📋 Что есть у нас":
        msg = "📋 У НАС ЕСТЬ:\n\n"
        for category, items in PRODUCTS.items():
            msg += f"{category}\n"
            for name in items:
                msg += f"• {name}\n"
            msg += "\n"
        await update.message.reply_text(msg, reply_markup=main_menu())
        return

    if text == "⬅️ Назад":
        context.user_data.clear()
        await update.message.reply_text(
            "Вы вернулись в главное меню 👇",
            reply_markup=main_menu()
        )
        return

    # Выбор категории
    if text in PRODUCTS:
        context.user_data["category"] = text
        await update.message.reply_text(
            CATEGORY_INFO.get(text, "Выберите товар 👇"),
            reply_markup=products_menu(text)
        )
        return

    # Выбор товара
    for category, items in PRODUCTS.items():
        if text in items:
            price = items[text]
            context.user_data["product"] = text
            context.user_data["price"] = price
            context.user_data["category"] = category

            msg = f"""
🛒 Вы выбрали:
{text}

📂 Категория:
{category}

💰 Цена:
{price}

{PAYMENT_TEXT}
"""
            await update.message.reply_text(msg, reply_markup=payment_menu())
            return

    # Кнопка оплаты
    if text == "✅ Я оплатил":
        product = context.user_data.get("product")
        price = context.user_data.get("price")
        category = context.user_data.get("category")

        if not product:
            await update.message.reply_text(
                "❌ Сначала выберите товар через кнопку «🛒 Купить».",
                reply_markup=main_menu()
            )
            return

        context.user_data["waiting_for_screenshot"] = True

        await update.message.reply_text(
            f"""📸 Теперь отправьте СКРИНШОТ оплаты.

📂 Категория: {category}
🛒 Товар: {product}
💰 Сумма: {price}

После отправки скрина заявка сразу уйдёт админу.""",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("⬅️ Назад")]],
                resize_keyboard=True
            )
        )
        return

    # Если непонятный текст
    await update.message.reply_text(
        "❌ Я не понял команду. Используйте кнопки ниже 👇",
        reply_markup=main_menu()
    )

# ---------------- ФОТО ----------------
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not context.user_data.get("waiting_for_screenshot"):
        await update.message.reply_text(
            "📸 Сначала выберите товар и нажмите «✅ Я оплатил».",
            reply_markup=main_menu()
        )
        return

    product = context.user_data.get("product", "Не указан")
    price = context.user_data.get("price", "Не указана")
    category = context.user_data.get("category", "Не указана")

    caption = f"""
🆕 НОВАЯ ЗАЯВКА НА ОПЛАТУ

👤 Клиент: {user.first_name}
🆔 ID: {user.id}
📎 Username: @{user.username if user.username else 'нет'}

📂 Категория: {category}
🛒 Товар: {product}
💰 Сумма: {price}
"""

    photo = update.message.photo[-1].file_id

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption
    )

    await update.message.reply_text(
        "✅ Скрин получен!\n\nАдмин проверит оплату и свяжется с вами.",
        reply_markup=main_menu()
    )

    context.user_data["waiting_for_screenshot"] = False

# ---------------- ОШИБКИ ----------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ошибка: {context.error}")

# ---------------- ЗАПУСК ----------------
def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден!")
    if not ADMIN_ID:
        raise ValueError("ADMIN_ID не найден!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error_handler)

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

SHOP_NAME = "UzbTopDonat"
SUPPORT_USERNAME = "@GGDONAT1"

# =========================
# ОПЛАТА
# =========================
PAYMENT_TEXT = """
💳 Оплата:

💳 Click / Payme / Карта:
5614 6805 0423 5934

👤 Получатель:
ARTIKOVA ZUXRA

📱 Номер телефона:
93 597 27 47

🏧 Можно оплатить через банкомат
❌ На номер НЕ кидать
🛑 За ошибочный перевод не ручаемся

📌 После оплаты нажмите "✅ Я оплатил"
и отправьте чек (скриншот).
"""

# =========================
# ТОВАРЫ
# =========================
PRODUCTS = {
    "⭐ Telegram Stars": {
        "Telegram Stars 100⭐": 30000,
        "Telegram Stars 150⭐": 45000,
        "Telegram Stars 250⭐": 70000,
        "Telegram Stars 350⭐": 95000,
        "Telegram Stars 500⭐": 140000,
        "Telegram Stars 750⭐": 199000,
        "Telegram Stars 1000⭐": 285000,
    },

    "💎 Telegram Premium": {
        "Telegram Premium 1 месяц": 60000,
        "Telegram Premium 1 год": 480000,
    },

    "💎 Гемы Brawl Stars": {
        "Brawl Stars 30 гемов": 16000,
        "Brawl Stars 80 гемов": 40000,
        "Brawl Stars 170 гемов": 74000,
        "Brawl Stars 360 гемов": 145000,
        "Brawl Stars 950 гемов": 355000,
        "Brawl Stars 2000 гемов": 685000,
    },

    "🔥 Brawl Pass": {
        "Brawl Pass": 70000,
        "Brawl Pass Plus": 110000,
    },

    "⚽ FC Points": {
        "FC Points 40+40": 13000,
        "FC Points 100+100": 25000,
        "FC Points 500+500": 96000,
        "FC Points 1000+1000": 195000,
        "FC Points 2000+2000": 380000,
    },

    "🌟 Звёздный абонемент": {
        "Звёздный абонемент": 195000,
        "Звёздный абонемент +20 уровней": 370000,
    }
}

# =========================
# АКЦИИ / ПРАЙС / ТЕКСТЫ
# =========================
ACTIONS_TEXT = """
🎁 АКЦИИ И ПРЕДЛОЖЕНИЯ

⭐ TELEGRAM STARS — ВЫГОДНО И БЫСТРО ⭐

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

📩 Заказ: @GGDONAT1
"""

PRICE_TEXT = """
💰 ПРАЙС

⭐ TELEGRAM STARS
• 100 ⭐ — 30 000 сум
• 150 ⭐ — 45 000 сум
• 250 ⭐ — 70 000 сум
• 350 ⭐ — 95 000 сум
• 500 ⭐ — 140 000 сум
• 750 ⭐ — 199 000 сум
• 1000 ⭐ — 285 000 сум

💎 TELEGRAM PREMIUM
• 1 месяц — 60 000 сум
• 1 год — 480 000 сум

💎 ГЕМЫ BRAWL STARS
• 30 гемов — 16 000 сум
• 80 гемов — 40 000 сум
• 170 гемов — 74 000 сум
• 360 гемов — 145 000 сум
• 950 гемов — 355 000 сум
• 2000 гемов — 685 000 сум

🔥 BRAWL PASS
• Brawl Pass — 70 000 сум
• Brawl Pass Plus — 110 000 сум

⚽ FC POINTS
• 40+40 — 13 000 сум
• 100+100 — 25 000 сум
• 500+500 — 96 000 сум
• 1000+1000 — 195 000 сум
• 2000+2000 — 380 000 сум

🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ
• Абонемент — 195 000 сум
• +20 уровней — 370 000 сум
"""

WHAT_WE_HAVE_TEXT = """
📋 ЧТО ЕСТЬ У НАС

⭐ Telegram Stars
💎 Telegram Premium
💎 Гемы Brawl Stars
🔥 Brawl Pass
⚽ FC Points
🌟 Звёздный абонемент

📩 Заказ и поддержка:
@GGDONAT1
"""

REVIEWS_TEXT = """
⭐ ОТЗЫВЫ

Отзывы можешь добавить вручную позже.
Пока можно написать сюда:

"Отзывы скоро будут 🔥"

Или просто отправлять клиентов в канал / чат с отзывами.
"""

SUPPORT_TEXT = f"""
🛠 Поддержка

Если есть вопросы или проблемы с заказом:
📩 Пиши: {SUPPORT_USERNAME}
"""

# =========================
# КЛАВИАТУРЫ
# =========================
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

def categories_menu():
    buttons = [[KeyboardButton(cat)] for cat in PRODUCTS.keys()]
    buttons.append([KeyboardButton("⬅️ Назад")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def products_menu(category):
    buttons = [[KeyboardButton(name)] for name in PRODUCTS[category].keys()]
    buttons.append([KeyboardButton("⬅️ Назад")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def after_payment_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("✅ Я оплатил")],
            [KeyboardButton("⬅️ Назад в меню")]
        ],
        resize_keyboard=True
    )

# =========================
# КОМАНДЫ
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    text = f"""
👋 Добро пожаловать в {SHOP_NAME}

Здесь можно купить:
⭐ Stars
💎 Premium
🎮 Игровые товары
⚽ FC Points

Выбери нужный раздел ниже 👇
"""
    await update.message.reply_text(text, reply_markup=main_menu())

# =========================
# ОБРАБОТКА ТЕКСТА
# =========================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Главное меню
    if text == "🛒 Купить":
        await update.message.reply_text(
            "📂 Выберите категорию:",
            reply_markup=categories_menu()
        )
        return

    elif text == "💰 Прайс":
        await update.message.reply_text(PRICE_TEXT, reply_markup=main_menu())
        return

    elif text == "🎁 Акции":
        await update.message.reply_text(ACTIONS_TEXT, reply_markup=main_menu())
        return

    elif text == "📦 Мои заказы":
        await update.message.reply_text(
            "📦 Ваши заказы пока не сохраняются в списке.\n\nНо после оплаты чек и заказ сразу приходят админу.",
            reply_markup=main_menu()
        )
        return

    elif text == "⭐ Отзывы":
        await update.message.reply_text(REVIEWS_TEXT, reply_markup=main_menu())
        return

    elif text == "🛠 Поддержка":
        await update.message.reply_text(SUPPORT_TEXT, reply_markup=main_menu())
        return

    elif text == "📋 Что есть у нас":
        await update.message.reply_text(WHAT_WE_HAVE_TEXT, reply_markup=main_menu())
        return

    elif text == "⬅️ Назад":
        await update.message.reply_text("🏠 Главное меню", reply_markup=main_menu())
        return

    elif text == "⬅️ Назад в меню":
        await update.message.reply_text("🏠 Главное меню", reply_markup=main_menu())
        return

    # Выбор категории
    if text in PRODUCTS:
        context.user_data["selected_category"] = text
        await update.message.reply_text(
            f"📦 Категория: {text}\n\nВыберите товар:",
            reply_markup=products_menu(text)
        )
        return

    # Выбор товара
    for category, items in PRODUCTS.items():
        if text in items:
            price = items[text]
            context.user_data["selected_product"] = text
            context.user_data["selected_price"] = price

            msg = f"""
🛒 Ваш товар:
{text}

💰 Цена:
{price:,} сум

{PAYMENT_TEXT}
"""
            await update.message.reply_text(msg, reply_markup=after_payment_menu())
            return

    # Кнопка "Я оплатил"
    elif text == "✅ Я оплатил":
        product = context.user_data.get("selected_product")
        price = context.user_data.get("selected_price")

        if not product:
            await update.message.reply_text(
                "❌ Сначала выберите товар.",
                reply_markup=main_menu()
            )
            return

        context.user_data["waiting_for_receipt"] = True

        await update.message.reply_text(
            f"""
📌 Вы выбрали:
🛒 {product}
💰 {price:,} сум

Теперь отправьте сюда:
📸 СКРИНШОТ ЧЕКА

После этого заказ автоматически уйдёт админу.
""",
            reply_markup=after_payment_menu()
        )
        return

    # Если не понял
    await update.message.reply_text(
        "❌ Я не понял команду. Используйте кнопки ниже 👇",
        reply_markup=main_menu()
    )

# =========================
# ОБРАБОТКА ФОТО (ЧЕК)
# =========================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_for_receipt"):
        await update.message.reply_text(
            "📸 Если это чек, сначала нажмите кнопку «✅ Я оплатил».",
            reply_markup=main_menu()
        )
        return

    user = update.effective_user
    product = context.user_data.get("selected_product", "Не указано")
    price = context.user_data.get("selected_price", 0)

    caption_to_admin = f"""
🚨 НОВЫЙ ЗАКАЗ

👤 Имя: {user.first_name or "Без имени"}
🆔 ID: {user.id}
📛 Username: @{user.username if user.username else "нет"}

🛒 Товар: {product}
💰 Сумма: {price:,} сум

📸 Ниже чек от клиента.
"""

    # Пересылаем фото админу
    try:
        photo = update.message.photo[-1].file_id
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=caption_to_admin
        )
    except Exception as e:
        print("Ошибка отправки админу:", e)

    # Сообщение клиенту
    await update.message.reply_text(
        f"""
✅ Чек получен!

Ваш заказ отправлен админу.

🛒 Товар: {product}
💰 Сумма: {price:,} сум

📩 Ожидайте подтверждения.
Если нужно ускорить — напишите {SUPPORT_USERNAME}
""",
        reply_markup=main_menu()
    )

    # Сброс
    context.user_data["waiting_for_receipt"] = False
    context.user_data["selected_product"] = None
    context.user_data["selected_price"] = None

# =========================
# ОБРАБОТКА ДОКУМЕНТОВ (если чек как файл)
# =========================
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_for_receipt"):
        await update.message.reply_text(
            "📎 Если это чек, сначала нажмите кнопку «✅ Я оплатил».",
            reply_markup=main_menu()
        )
        return

    user = update.effective_user
    product = context.user_data.get("selected_product", "Не указано")
    price = context.user_data.get("selected_price", 0)

    caption_to_admin = f"""
🚨 НОВЫЙ ЗАКАЗ

👤 Имя: {user.first_name or "Без имени"}
🆔 ID: {user.id}
📛 Username: @{user.username if user.username else "нет"}

🛒 Товар: {product}
💰 Сумма: {price:,} сум

📎 Клиент отправил чек файлом.
"""

    try:
        document = update.message.document.file_id
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=document,
            caption=caption_to_admin
        )
    except Exception as e:
        print("Ошибка отправки файла админу:", e)

    await update.message.reply_text(
        f"""
✅ Чек получен!

Ваш заказ отправлен админу.

🛒 Товар: {product}
💰 Сумма: {price:,} сум

📩 Ожидайте подтверждения.
Если нужно ускорить — напишите {SUPPORT_USERNAME}
""",
        reply_markup=main_menu()
    )

    context.user_data["waiting_for_receipt"] = False
    context.user_data["selected_product"] = None
    context.user_data["selected_price"] = None

# =========================
# ЗАПУСК
# =========================
def main():
    print("Бот запущен...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()

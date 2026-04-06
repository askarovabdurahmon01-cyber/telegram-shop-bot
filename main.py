import os
import json
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

SHOP_NAME = "GG DONAT SHOP"
SUPPORT_USERNAME = "@GGDONAT1"

ORDERS_FILE = "orders.json"

# -------------------------
# ТОВАРЫ
# -------------------------
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

    "🎮 Гемы Brawl Stars": {
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

# -------------------------
# СОСТОЯНИЯ
# -------------------------
user_state = {}  # user_id -> category
user_orders = {}  # user_id -> [orders]


# -------------------------
# ФАЙЛ ЗАКАЗОВ
# -------------------------
def load_orders():
    global user_orders
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                user_orders = json.load(f)
        except:
            user_orders = {}
    else:
        user_orders = {}

def save_orders():
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(user_orders, f, ensure_ascii=False, indent=2)


# -------------------------
# КЛАВИАТУРЫ
# -------------------------
def main_menu():
    keyboard = [
        [KeyboardButton("🛒 Купить"), KeyboardButton("💰 Прайс")],
        [KeyboardButton("🎁 Акции"), KeyboardButton("📦 Мои заказы")],
        [KeyboardButton("⭐ Отзывы"), KeyboardButton("🛠 Поддержка")],
        [KeyboardButton("📋 Что есть у нас")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def categories_menu():
    keyboard = [[KeyboardButton(cat)] for cat in PRODUCTS.keys()]
    keyboard.append([KeyboardButton("⬅️ Назад")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def products_menu(category):
    keyboard = [[KeyboardButton(name)] for name in PRODUCTS[category].keys()]
    keyboard.append([KeyboardButton("⬅️ Назад")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# -------------------------
# ТЕКСТЫ
# -------------------------
def get_price_text():
    return """💰 ПРАЙС ЛИСТ 💰

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

🎮 ГЕМЫ BRAWL STARS
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
• 40 + 40 — 13 000 сум
• 100 + 100 — 25 000 сум
• 500 + 500 — 96 000 сум
• 1000 + 1000 — 195 000 сум
• 2000 + 2000 — 380 000 сум

🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ
• Абонемент — 195 000 сум
• +20 уровней — 370 000 сум
"""

def get_promo_text():
    return """🎁 АКЦИИ 🎁

🔥 Успей купить по текущим ценам
🔥 Некоторые товары идут по скидке
🔥 FC Points сейчас с двойным бонусом

📩 Заказ: @GGDONAT1
"""

def get_reviews_text():
    return """⭐ ОТЗЫВЫ ⭐

Отзывы клиентов можно посмотреть у администратора 👇
📩 @GGDONAT1
"""

def get_support_text():
    return f"""🛠 ПОДДЕРЖКА

Если есть вопросы или проблемы:
📩 Пиши сюда: {SUPPORT_USERNAME}
"""

def get_catalog_text():
    text = "📋 ЧТО ЕСТЬ У НАС:\n\n"
    for category, items in PRODUCTS.items():
        text += f"{category}\n"
        for item, price in items.items():
            text += f"• {item} — {price:,} сум\n".replace(",", " ")
        text += "\n"
    return text


# -------------------------
# КОМАНДЫ
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Добро пожаловать в {SHOP_NAME}!\n\n"
        f"Выбери нужный раздел ниже 👇",
        reply_markup=main_menu()
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📍 Главное меню", reply_markup=main_menu())

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_price_text(), reply_markup=main_menu())

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛒 Выбери категорию товара:",
        reply_markup=categories_menu()
    )

async def promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_promo_text(), reply_markup=main_menu())

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_support_text(), reply_markup=main_menu())

async def reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_reviews_text(), reply_markup=main_menu())

async def myorders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    orders = user_orders.get(user_id, [])

    if not orders:
        await update.message.reply_text("📦 У тебя пока нет заказов.", reply_markup=main_menu())
        return

    text = "📦 ТВОИ ЗАКАЗЫ:\n\n"
    for i, order in enumerate(orders, 1):
        text += f"{i}. {order}\n"

    await update.message.reply_text(text, reply_markup=main_menu())


# -------------------------
# ОБРАБОТКА ТЕКСТА
# -------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    user_id = str(user.id)

    # Главное меню
    if text == "🛒 Купить":
        await update.message.reply_text("🛒 Выбери категорию товара:", reply_markup=categories_menu())
        return

    elif text == "💰 Прайс":
        await update.message.reply_text(get_price_text(), reply_markup=main_menu())
        return

    elif text == "🎁 Акции":
        await update.message.reply_text(get_promo_text(), reply_markup=main_menu())
        return

    elif text == "📦 Мои заказы":
        orders = user_orders.get(user_id, [])
        if not orders:
            await update.message.reply_text("📦 У тебя пока нет заказов.", reply_markup=main_menu())
        else:
            msg = "📦 ТВОИ ЗАКАЗЫ:\n\n"
            for i, order in enumerate(orders, 1):
                msg += f"{i}. {order}\n"
            await update.message.reply_text(msg, reply_markup=main_menu())
        return

    elif text == "⭐ Отзывы":
        await update.message.reply_text(get_reviews_text(), reply_markup=main_menu())
        return

    elif text == "🛠 Поддержка":
        await update.message.reply_text(get_support_text(), reply_markup=main_menu())
        return

    elif text == "📋 Что есть у нас":
        await update.message.reply_text(get_catalog_text(), reply_markup=main_menu())
        return

    elif text == "⬅️ Назад":
        user_state.pop(user_id, None)
        await update.message.reply_text("⬅️ Возврат в меню", reply_markup=main_menu())
        return

    # Если выбрал категорию
    if text in PRODUCTS:
        user_state[user_id] = text
        await update.message.reply_text(
            f"📂 Категория: {text}\n\nВыбери товар кнопкой 👇",
            reply_markup=products_menu(text)
        )
        return

    # Если выбрал товар
    if user_id in user_state:
        category = user_state[user_id]

        if text in PRODUCTS[category]:
            price = PRODUCTS[category][text]

            order_text = (
                f"🛒 НОВЫЙ ЗАКАЗ\n\n"
                f"👤 Клиент: @{user.username if user.username else 'нет username'}\n"
                f"🆔 ID: {user.id}\n"
                f"📦 Товар: {text}\n"
                f"💰 Цена: {price:,} сум".replace(",", " ")
            )

            # отправка админу
            await context.bot.send_message(chat_id=ADMIN_ID, text=order_text)

            # сохраняем заказ
            if user_id not in user_orders:
                user_orders[user_id] = []

            user_orders[user_id].append(f"{text} — {price:,} сум".replace(",", " "))
            save_orders()

            await update.message.reply_text(
                f"✅ Заказ оформлен!\n\n"
                f"📦 Товар: {text}\n"
                f"💰 Цена: {price:,} сум\n\n"
                f"📩 Для оплаты напиши: {SUPPORT_USERNAME}".replace(",", " "),
                reply_markup=main_menu()
            )

            user_state.pop(user_id, None)
            return
        else:
            await update.message.reply_text(
                "❌ Выбирай товар только кнопками ниже 👇",
                reply_markup=products_menu(category)
            )
            return

    await update.message.reply_text(
        "❌ Нажми нужную кнопку ниже 👇",
        reply_markup=main_menu()
    )


# -------------------------
# ЗАПУСК
# -------------------------
def main():
    load_orders()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("promo", promo))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(CommandHandler("reviews", reviews))
    app.add_handler(CommandHandler("myorders", myorders))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()

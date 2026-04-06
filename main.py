import json
import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

SHOP_NAME = "GG DONAT SHOP"
SUPPORT_USERNAME = "@GGDONAT1"
PAYMENT_TEXT = "Оплата: Click / Payme / Карта"

# -----------------------
# ТОВАРЫ
# -----------------------
PRODUCTS = {
    "Telegram Stars 100⭐": 30000,
    "Telegram Stars 150⭐": 45000,
    "Telegram Stars 250⭐": 70000,
    "Telegram Stars 350⭐": 95000,
    "Telegram Stars 500⭐": 140000,
    "Telegram Stars 750⭐": 199000,
    "Telegram Stars 1000⭐": 285000,

    "Telegram Premium 1 месяц": 60000,
    "Telegram Premium 1 год": 480000,

    "Brawl Stars 30 гемов": 16000,
    "Brawl Stars 80 гемов": 40000,
    "Brawl Stars 170 гемов": 74000,
    "Brawl Stars 360 гемов": 145000,
    "Brawl Stars 950 гемов": 355000,
    "Brawl Stars 2000 гемов": 685000,

    "Brawl Pass": 70000,
    "Brawl Pass Plus": 110000,

    "FC Points 40+40": 13000,
    "FC Points 100+100": 25000,
    "FC Points 500+500": 96000,
    "FC Points 1000+1000": 195000,
    "FC Points 2000+2000": 380000,

    "Звёздный абонемент": 195000,
    "Звёздный абонемент +20 уровней": 370000
}

# -----------------------
# КАТЕГОРИИ
# -----------------------
CATEGORIES = {
    "⭐ Telegram Stars": [
        "Telegram Stars 100⭐",
        "Telegram Stars 150⭐",
        "Telegram Stars 250⭐",
        "Telegram Stars 350⭐",
        "Telegram Stars 500⭐",
        "Telegram Stars 750⭐",
        "Telegram Stars 1000⭐"
    ],
    "💎 Telegram Premium": [
        "Telegram Premium 1 месяц",
        "Telegram Premium 1 год"
    ],
    "💎 Гемы Brawl Stars": [
        "Brawl Stars 30 гемов",
        "Brawl Stars 80 гемов",
        "Brawl Stars 170 гемов",
        "Brawl Stars 360 гемов",
        "Brawl Stars 950 гемов",
        "Brawl Stars 2000 гемов"
    ],
    "🔥 Brawl Pass": [
        "Brawl Pass",
        "Brawl Pass Plus"
    ],
    "⚽ FC Points": [
        "FC Points 40+40",
        "FC Points 100+100",
        "FC Points 500+500",
        "FC Points 1000+1000",
        "FC Points 2000+2000"
    ],
    "🌟 Звёздный абонемент": [
        "Звёздный абонемент",
        "Звёздный абонемент +20 уровней"
    ]
}

ORDERS_FILE = "orders.json"
user_data_temp = {}

# -----------------------
# ФАЙЛ ЗАКАЗОВ
# -----------------------
def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

# -----------------------
# МЕНЮ
# -----------------------
def main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🛒 Купить"), KeyboardButton("💰 Прайс")],
            [KeyboardButton("🎁 Акции"), KeyboardButton("📦 Мои заказы")],
            [KeyboardButton("⭐ Отзывы"), KeyboardButton("🛠 Поддержка")],
            [KeyboardButton("📋 Что есть у нас")]
        ],
        resize_keyboard=True
    )

# -----------------------
# КОМАНДЫ
# -----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"👋 Добро пожаловать в {SHOP_NAME}!\n\n"
        "🔥 Здесь ты можешь купить:\n"
        "• Telegram Stars\n"
        "• Telegram Premium\n"
        "• Brawl Stars гемы\n"
        "• Brawl Pass\n"
        "• FC Points\n"
        "• Звёздный абонемент\n\n"
        "Выбери нужный раздел ниже 👇"
    )
    await update.message.reply_text(text, reply_markup=main_menu())

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Главное меню:", reply_markup=main_menu())

async def what_we_have(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📋 ЧТО ЕСТЬ У НАС:\n\n"
        "⭐ Telegram Stars\n"
        "💎 Telegram Premium\n"
        "💎 Гемы Brawl Stars\n"
        "🔥 Brawl Pass / Brawl Pass Plus\n"
        "⚽ FC Points\n"
        "🌟 Звёздный абонемент\n\n"
        "Нажми /price чтобы посмотреть цены\n"
        "Или /buy чтобы оформить заказ"
    )
    await update.message.reply_text(text)

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💰 ПРАЙС:\n\n"

        "⭐ TELEGRAM STARS:\n"
        "• 100 ⭐ — 30 000 сум\n"
        "• 150 ⭐ — 45 000 сум\n"
        "• 250 ⭐ — 70 000 сум\n"
        "• 350 ⭐ — 95 000 сум\n"
        "• 500 ⭐ — 140 000 сум\n"
        "• 750 ⭐ — 199 000 сум\n"
        "• 1000 ⭐ — 285 000 сум\n\n"

        "💎 TELEGRAM PREMIUM:\n"
        "• 1 месяц — 60 000 сум\n"
        "• 1 год — 480 000 сум\n\n"

        "💎 ГЕМЫ BRAWL STARS:\n"
        "• 30 гемов — 16 000 сум\n"
        "• 80 гемов — 40 000 сум\n"
        "• 170 гемов — 74 000 сум\n"
        "• 360 гемов — 145 000 сум\n"
        "• 950 гемов — 355 000 сум\n"
        "• 2000 гемов — 685 000 сум\n\n"

        "🔥 BRAWL PASS:\n"
        "• Brawl Pass — 70 000 сум\n"
        "• Brawl Pass Plus — 110 000 сум\n\n"

        "⚽ FC POINTS:\n"
        "• 40 + 40 — 13 000 сум\n"
        "• 100 + 100 — 25 000 сум\n"
        "• 500 + 500 — 96 000 сум\n"
        "• 1000 + 1000 — 195 000 сум\n"
        "• 2000 + 2000 — 380 000 сум\n\n"

        "🌟 ЗВЁЗДНЫЙ АБОНЕМЕНТ:\n"
        "• Абонемент — 195 000 сум\n"
        "• +20 уровней — 370 000 сум"
    )
    await update.message.reply_text(text)

async def promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎁 АКЦИИ:\n\n"
        "🔥 Brawl Pass по выгодной цене\n"
        "🔥 FC Points с бонусом x2\n"
        "🔥 Telegram Stars по актуальным ценам\n\n"
        "⚡ Успей купить, пока цена не изменилась!"
    )

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🛠 Поддержка:\n\n"
        f"Если есть вопросы или нужна оплата — пиши сюда:\n{SUPPORT_USERNAME}"
    )

async def reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⭐ Отзывы:\n\n"
        f"Чтобы посмотреть или отправить отзывы, пиши:\n{SUPPORT_USERNAME}"
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛒 ПОКУПКА\n\n"
        "Выбери категорию и напиши её точно:\n\n"
        "⭐ Telegram Stars\n"
        "💎 Telegram Premium\n"
        "💎 Гемы Brawl Stars\n"
        "🔥 Brawl Pass\n"
        "⚽ FC Points\n"
        "🌟 Звёздный абонемент"
    )
    user_data_temp[update.effective_user.id] = {"step": "choose_category"}
    await update.message.reply_text(text)

async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    all_orders = load_orders()
    my_orders = [o for o in all_orders if o["telegram_id"] == user_id]

    if not my_orders:
        await update.message.reply_text("📦 У тебя пока нет заказов.")
        return

    text = "📦 ТВОИ ЗАКАЗЫ:\n\n"
    for order in my_orders[-10:]:
        text += (
            f"🧾 Заказ #{order['order_id']}\n"
            f"📦 Товар: {order['product']}\n"
            f"💰 Цена: {order['price']} сум\n"
            f"🆔 ID / Username: {order['game_id']}\n"
            f"📌 Статус: {order['status']}\n\n"
        )

    await update.message.reply_text(text)

# -----------------------
# ОБРАБОТКА СООБЩЕНИЙ
# -----------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Кнопки
    if text == "🛒 Купить":
        await buy(update, context)
        return
    elif text == "💰 Прайс":
        await price(update, context)
        return
    elif text == "🎁 Акции":
        await promo(update, context)
        return
    elif text == "📦 Мои заказы":
        await orders(update, context)
        return
    elif text == "⭐ Отзывы":
        await reviews(update, context)
        return
    elif text == "🛠 Поддержка":
        await support(update, context)
        return
    elif text == "📋 Что есть у нас":
        await what_we_have(update, context)
        return

    if user_id in user_data_temp:
        step = user_data_temp[user_id].get("step")

        # 1. Выбор категории
        if step == "choose_category":
            if text not in CATEGORIES:
                await update.message.reply_text("❌ Такой категории нет. Напиши точно как в списке.")
                return

            user_data_temp[user_id]["category"] = text
            user_data_temp[user_id]["step"] = "choose_product"

            products_list = "\n".join([f"• {p}" for p in CATEGORIES[text]])

            await update.message.reply_text(
                f"📦 Категория: {text}\n\n"
                f"Выбери товар и напиши его точно:\n\n{products_list}"
            )
            return

        # 2. Выбор товара
        elif step == "choose_product":
            category = user_data_temp[user_id]["category"]

            if text not in CATEGORIES[category]:
                await update.message.reply_text("❌ Такого товара нет в этой категории. Напиши точно как в списке.")
                return

            user_data_temp[user_id]["product"] = text
            user_data_temp[user_id]["price"] = PRODUCTS[text]
            user_data_temp[user_id]["step"] = "enter_game_id"

            await update.message.reply_text(
                f"✅ Выбран товар: {text}\n"
                f"💰 Цена: {PRODUCTS[text]:,} сум\n\n"
                "Теперь отправь свой Telegram username / игровой ID / UID:".replace(",", " ")
            )
            return

        # 3. Ввод ID
        elif step == "enter_game_id":
            user_data_temp[user_id]["game_id"] = text
            user_data_temp[user_id]["step"] = "confirm_order"

            product = user_data_temp[user_id]["product"]
            price_value = user_data_temp[user_id]["price"]

            await update.message.reply_text(
                f"🧾 Подтверждение заказа:\n\n"
                f"📦 Товар: {product}\n"
                f"💰 Цена: {price_value:,} сум\n"
                f"🆔 ID / Username: {text}\n\n"
                f"💳 {PAYMENT_TEXT}\n\n"
                "Чтобы подтвердить заказ, напиши:\nCONFIRM".replace(",", " ")
            )
            return

        # 4. Подтверждение
        elif step == "confirm_order":
            if text.upper() != "CONFIRM":
                await update.message.reply_text("❌ Напиши именно: CONFIRM")
                return

            all_orders = load_orders()
            order_id = len(all_orders) + 1

            username = update.effective_user.username
            if username:
                username = f"@{username}"
            else:
                username = "без username"

            order = {
                "order_id": order_id,
                "telegram_id": user_id,
                "username": username,
                "product": user_data_temp[user_id]["product"],
                "price": user_data_temp[user_id]["price"],
                "game_id": user_data_temp[user_id]["game_id"],
                "status": "Ожидает оплаты"
            }

            all_orders.append(order)
            save_orders(all_orders)

            await update.message.reply_text(
                f"✅ Заказ создан!\n\n"
                f"🧾 Номер заказа: #{order_id}\n"
                f"📦 Товар: {order['product']}\n"
                f"💰 Цена: {order['price']} сум\n"
                f"📌 Статус: {order['status']}\n\n"
                f"📩 Для оплаты и подтверждения пиши сюда:\n{SUPPORT_USERNAME}",
                reply_markup=main_menu()
            )

            if ADMIN_ID != 0:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=(
                        f"🛒 НОВЫЙ ЗАКАЗ!\n\n"
                        f"🧾 Заказ #{order_id}\n"
                        f"👤 Клиент: {username}\n"
                        f"📦 Товар: {order['product']}\n"
                        f"💰 Цена: {order['price']} сум\n"
                        f"🆔 ID / Username: {order['game_id']}\n"
                        f"📌 Статус: {order['status']}"
                    )
                )

            del user_data_temp[user_id]
            return

    await update.message.reply_text(
        "❓ Я не понял команду.\n\n"
        "Используй меню или команды:\n"
        "/start /menu /price /buy /promo /support /reviews /orders"
    )

# -----------------------
# ЗАПУСК
# -----------------------
def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден. Добавь его в Railway Variables.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("promo", promo))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(CommandHandler("reviews", reviews))
    app.add_handler(CommandHandler("orders", orders))
    app.add_handler(CommandHandler("whatis", what_we_have))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main() 

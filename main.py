import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
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

# Категории и товары
PRODUCTS = {
    "⭐ Telegram Stars": {
        "Telegram Stars 100⭐": "40 000 сум",
        "Telegram Stars 150⭐": "60 000 сум",
        "Telegram Stars 250⭐": "95 000 сум",
        "Telegram Stars 350⭐": "130 000 сум",
        "Telegram Stars 500⭐": "180 000 сум",
        "Telegram Stars 750⭐": "260 000 сум",
        "Telegram Stars 1000⭐": "340 000 сум",
    },
    "💎 Голда": {
        "400 Голды": "40 000 сум",
        "800 Голды": "75 000 сум",
        "1200 Голды": "110 000 сум",
    },
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
            [KeyboardButton("⭐ Telegram Stars"), KeyboardButton("💎 Голда")],
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

Добро пожаловать в магазин.

Выберите нужный раздел ниже 👇
"""
    await update.message.reply_text(text, reply_markup=main_menu())

# ---------------- ОБРАБОТКА ТЕКСТА ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    # Главное меню
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
        msg = "💰 Наш прайс:\n\n"
        for category, items in PRODUCTS.items():
            msg += f"{category}\n"
            for name, price in items.items():
                msg += f"• {name} — {price}\n"
            msg += "\n"
        await update.message.reply_text(msg, reply_markup=main_menu())
        return

    if text == "🎁 Акции":
        await update.message.reply_text(
            "🎁 Сейчас акции уточняйте у поддержки.",
            reply_markup=main_menu()
        )
        return

    if text == "📦 Мои заказы":
        await update.message.reply_text(
            "📦 Пока у вас нет сохранённых заказов.",
            reply_markup=main_menu()
        )
        return

    if text == "⭐ Отзывы":
        await update.message.reply_text(
            "⭐ Отзывы можно добавить позже.",
            reply_markup=main_menu()
        )
        return

    if text == "🛠 Поддержка":
        await update.message.reply_text(
            "🛠 Если есть вопросы — напишите сюда, и админ увидит.",
            reply_markup=main_menu()
        )
        return

    if text == "📋 Что есть у нас":
        msg = "📋 У нас есть:\n\n"
        for category, items in PRODUCTS.items():
            msg += f"{category}\n"
            for name in items:
                msg += f"• {name}\n"
            msg += "\n"
        await update.message.reply_text(msg, reply_markup=main_menu())
        return

    # Назад
    if text == "⬅️ Назад":
        await update.message.reply_text(
            "Вы вернулись в главное меню 👇",
            reply_markup=main_menu()
        )
        context.user_data.clear()
        return

    # Категории
    if text in PRODUCTS:
        context.user_data["category"] = text
        await update.message.reply_text(
            f"Выберите товар из категории {text} 👇",
            reply_markup=products_menu(text)
        )
        return

    # Товары
    for category, items in PRODUCTS.items():
        if text in items:
            price = items[text]
            context.user_data["product"] = text
            context.user_data["price"] = price

            msg = f"""
🛒 Ваш товар:
{text}

💰 Цена:
{price}

{PAYMENT_TEXT}
"""
            await update.message.reply_text(msg, reply_markup=payment_menu())
            return

    # Я оплатил
    if text == "✅ Я оплатил":
        product = context.user_data.get("product")
        price = context.user_data.get("price")

        if not product:
            await update.message.reply_text(
                "❌ Сначала выберите товар через кнопку «Купить».",
                reply_markup=main_menu()
            )
            return

        context.user_data["waiting_for_screenshot"] = True

        await update.message.reply_text(
            f"""📸 Теперь отправьте СКРИНШОТ оплаты.

🛒 Товар: {product}
💰 Сумма: {price}

После отправки скрина заявка уйдёт админу.""",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("⬅️ Назад")]],
                resize_keyboard=True
            )
        )
        return

    # Если текст не распознан
    await update.message.reply_text(
        "❌ Я не понял команду. Нажмите кнопку ниже 👇",
        reply_markup=main_menu()
    )

# ---------------- ОБРАБОТКА ФОТО ----------------
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

    caption = f"""
🆕 НОВАЯ ЗАЯВКА НА ОПЛАТУ

👤 Клиент: {user.first_name}
🆔 ID: {user.id}
📎 Username: @{user.username if user.username else 'нет'}

🛒 Товар: {product}
💰 Сумма: {price}
"""

    # Берём самое большое фото
    photo = update.message.photo[-1].file_id

    # Отправка админу
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption
    )

    # Клиенту
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

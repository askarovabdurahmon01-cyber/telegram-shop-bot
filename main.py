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
# ТОВАРЫ
# =========================
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
    "Звёздный абонемент +20 уровней": 370000,
}

# =========================
# КАТЕГОРИИ
# =========================
CATEGORIES = {
    "⭐ Telegram Stars": [
        "Telegram Stars 100⭐",
        "Telegram Stars 150⭐",
        "Telegram Stars 250⭐",
        "Telegram Stars 350⭐",
        "Telegram Stars 500⭐",
        "Telegram Stars 750⭐",
        "Telegram Stars 1000⭐",
    ],
    "⭐ Telegram Premium": [
        "Telegram Premium 1 месяц",
        "Telegram Premium 1 год",
    ],
    "💎 Гемы Brawl Stars": [
        "Brawl Stars 30 гемов",
        "Brawl Stars 80 гемов",
        "Brawl Stars 170 гемов",
        "Brawl Stars 360 гемов",
        "Brawl Stars 950 гемов",
        "Brawl Stars 2000 гемов",
    ],
    "🔥 Brawl Pass": [
        "Brawl Pass",
        "Brawl Pass Plus",
    ],
    "⚽ FC Points": [
        "FC Points 40+40",
        "FC Points 100+100",
        "FC Points 500+500",
        "FC Points 1000+1000",
        "FC Points 2000+2000",
    ],
    "🌟 Звёздный абонемент": [
        "Звёздный абонемент",
        "Звёздный абонемент +20 уровней",
    ],
}

# =========================
# КНОПКИ
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
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("⭐ Telegram Stars"), KeyboardButton("⭐ Telegram Premium")],
            [KeyboardButton("💎 Гемы Brawl Stars"), KeyboardButton("🔥 Brawl Pass")],
            [KeyboardButton("⚽ FC Points"), KeyboardButton("🌟 Звёздный абонемент")],
            [KeyboardButton("🔙 Назад")],
        ],
        resize_keyboard=True
    )

def payment_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("☑️ Я оплатил")],
            [KeyboardButton("🔙 Назад")],
        ],
        resize_keyboard=True
    )

# =========================
# /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name if update.effective_user else "друг"

    text = f"""
👋 Привет, {user}!

Добро пожаловать в <b>{SHOP_NAME}</b> 🚀

Здесь ты можешь быстро купить:
⭐ Telegram Stars
⭐ Telegram Premium
💎 Гемы Brawl Stars
🔥 Brawl Pass
⚽ FC Points
🌟 Звёздный абонемент

Выбери нужный раздел ниже 👇
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# =========================
# ТЕКСТ
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip() if update.message.text else ""

    # Главное меню
    if text == "🛒 Купить":
        await update.message.reply_text(
            "🛍 Выбери категорию:",
            reply_markup=categories_menu()
        )

    elif text == "💰 Прайс":
        msg = "💰 <b>Наш прайс:</b>\n\n"
        for category, items in CATEGORIES.items():
            msg += f"<b>{category}</b>\n"
            for item in items:
                price = PRODUCTS.get(item, 0)
                msg += f"• {item} — <b>{price:,} сум</b>\n"
            msg += "\n"

        await update.message.reply_text(msg, parse_mode="HTML")

    elif text == "🎁 Акции":
        await update.message.reply_text(
            "🔥 <b>Сейчас действуют выгодные цены!</b>\n\n"
            "Успей купить по текущим ценам 🚀",
            parse_mode="HTML"
        )

    elif text == "📦 Мои заказы":
        await update.message.reply_text(
            "📦 История заказов пока не подключена.\n"
            "Но твои оплаты и чеки будут приходить админу."
        )

    elif text == "⭐ Отзывы":
        await update.message.reply_text(
            "⭐ Раздел отзывов пока в разработке."
        )

    elif text == "🛠 Поддержка":
        await update.message.reply_text(
            f"🛠 Поддержка: {SUPPORT_USERNAME}"
        )

    elif text == "📋 Что есть у нас":
        msg = "📋 <b>Что есть у нас:</b>\n\n"
        for category in CATEGORIES.keys():
            msg += f"• {category}\n"
        await update.message.reply_text(msg, parse_mode="HTML")

    elif text == "🔙 Назад":
        await start(update, context)

    # Категории
    elif text in CATEGORIES:
        items = "\n".join([f"• {item}" for item in CATEGORIES[text]])
        await update.message.reply_text(
            f"📦 <b>{text}</b>\n\n"
            f"Выбери товар и напиши его <b>ТОЧНО</b> как в списке:\n\n{items}",
            parse_mode="HTML"
        )

    # Выбор товара
    elif text in PRODUCTS:
        price = PRODUCTS[text]

        context.user_data["selected_product"] = text
        context.user_data["selected_price"] = price
        context.user_data["waiting_payment_proof"] = False

        pay_text = f"""
🛍 <b>Ваш заказ:</b>
{text}

💰 <b>Сумма:</b> {price:,} сум

💳 <b>Оплата:</b>

<b>Номер карты 💳 Click / Payme</b>
<code>5614680504235934</code>

<b>Получатель:</b>
ARTIKOVA ZUXRA

<b>Номер телефона 📱</b>
93 597 27 47

🏧 Можно в банкомате
❌ На номер не кидать

⚠️ <b>За ошибочный перевод не ручаюсь</b>

📌 <b>После оплаты:</b>
1) Оплати нужную сумму
2) Сделай скрин / фото чека
3) Нажми <b>☑️ Я оплатил</b>
4) Отправь чек сюда
"""

        await update.message.reply_text(
            pay_text,
            parse_mode="HTML",
            reply_markup=payment_menu()
        )

    elif text == "☑️ Я оплатил":
        selected_product = context.user_data.get("selected_product")
        selected_price = context.user_data.get("selected_price")

        if not selected_product:
            await update.message.reply_text(
                "❌ Сначала выбери товар через кнопку «🛒 Купить»."
            )
            return

        context.user_data["waiting_payment_proof"] = True

        await update.message.reply_text(
            f"📸 Отлично!\n\n"
            f"Теперь отправь сюда <b>СКРИНШОТ или ФОТО оплаты</b>.\n\n"
            f"🛍 Товар: <b>{selected_product}</b>\n"
            f"💰 Сумма: <b>{selected_price:,} сум</b>\n\n"
            f"После этого бот автоматически отправит чек админу.",
            parse_mode="HTML"
        )

    else:
        await update.message.reply_text(
            "❌ Такого товара нет в этой категории.\n"
            "Напиши точно как в списке."
        )

# =========================
# ФОТО ЧЕКА
# =========================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_payment_proof"):
        await update.message.reply_text(
            "📸 Сначала выбери товар и нажми «☑️ Я оплатил»."
        )
        return

    user = update.effective_user
    selected_product = context.user_data.get("selected_product", "Не выбран")
    selected_price = context.user_data.get("selected_price", 0)

    username = f"@{user.username}" if user.username else "нет username"

    caption = f"""
💸 <b>НОВАЯ ОПЛАТА</b>

👤 <b>Клиент:</b> {user.full_name}
📩 <b>Username:</b> {username}
🆔 <b>ID:</b> <code>{user.id}</code>

🛍 <b>Товар:</b> {selected_product}
💰 <b>Сумма:</b> {selected_price:,} сум

📌 Проверь оплату и свяжись с клиентом.
"""

    photo = update.message.photo[-1].file_id

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption,
        parse_mode="HTML"
    )

    await update.message.reply_text(
        "✅ <b>Чек отправлен админу!</b>\n\n"
        "⏳ Ожидай подтверждения и выдачи товара.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

    context.user_data["waiting_payment_proof"] = False

# =========================
# ДОКУМЕНТ (если чек отправят файлом)
# =========================
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_payment_proof"):
        await update.message.reply_text(
            "📄 Сначала выбери товар и нажми «☑️ Я оплатил»."
        )
        return

    user = update.effective_user
    selected_product = context.user_data.get("selected_product", "Не выбран")
    selected_price = context.user_data.get("selected_price", 0)

    username = f"@{user.username}" if user.username else "нет username"

    caption = f"""
💸 <b>НОВАЯ ОПЛАТА (ФАЙЛ)</b>

👤 <b>Клиент:</b> {user.full_name}
📩 <b>Username:</b> {username}
🆔 <b>ID:</b> <code>{user.id}</code>

🛍 <b>Товар:</b> {selected_product}
💰 <b>Сумма:</b> {selected_price:,} сум

📌 Проверь оплату и свяжись с клиентом.
"""

    document = update.message.document.file_id

    await context.bot.send_document(
        chat_id=ADMIN_ID,
        document=document,
        caption=caption,
        parse_mode="HTML"
    )

    await update.message.reply_text(
        "✅ <b>Чек отправлен админу!</b>\n\n"
        "⏳ Ожидай подтверждения и выдачи товара.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

    context.user_data["waiting_payment_proof"] = False

# =========================
# ОШИБКИ
# =========================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ошибка: {context.error}")

# =========================
# ЗАПУСК
# =========================
def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не найден")
        return

    if not ADMIN_ID:
        print("❌ ADMIN_ID не найден")
        return

    print("✅ Бот запущен...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error_handler)

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

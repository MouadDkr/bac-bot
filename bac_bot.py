
import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

# استخدم متغير البيئة للحصول على التوكن
BOT_TOKEN = os.getenv("BOT_TOKEN")

subjects_with_streams = {
    "📐 الرياضيات": ["رياضي", "تقني رياضي", "تسيير واقتصاد", "علمي", "الشعب الأدبية"],
    "🧪 العلوم الفيزيائية": ["رياضي/تقني رياضي", "علوم"],
    "🧬 علوم الطبيعة والحياة": ["رياضي", "علمي"],
    "📖 الفلسفة": ["رياضي/علمي", "تسيير واقتصاد/تقني رياضي", "فلسفة", "لغات"],
    "📜 التاريخ والجغرافيا": ["رياضي/تقني رياضي/علمي", "فلسفة", "لغات"],
    "📚 اللغة الفرنسية": ["الشعب العلمية", "فلسفة", "لغات"],
    "📚 اللغة الإنجليزية": ["الشعب العلمية", "فلسفة", "لغات"],
    "📚 اللغة العربية": ["الشعب العلمية", "فلسفة", "لغات"],
    "🌍 اللغة الإسبانية": [],
    "🌍 اللغة الألمانية": [],
    "📒 التسيير المحاسبي والمالي": [],
    "📊 الاقتصاد": [],
    "⚖️ القانون": [],
    "🏗️ الهندسة المدنية": [],
    "⚙️ الهندسة الميكانيكية": [],
    "🧪 هندسة الطرائق": [],
    "💡 الهندسة الكهربائية": [],
}

main_menu = [["📘 الملخصات"], ["📚 المواضيع"], ["📝 الباكالوريات"]]

topics_menu = [["📕 الفصل الأول", "📘 الفصل الثاني"], ["📙 الفصل الثالث", "📔 شامل"], ["⬅️ الرجوع"]]

def get_subjects_menu():
    subjects = list(subjects_with_streams.keys())
    menu = [subjects[i:i+2] for i in range(0, len(subjects), 2)]
    menu.append(["⬅️ الرجوع", "🏠 الرئيسية"])
    return menu

def get_years_menu():
    years = [str(year) for year in range(2008, 2026)]
    menu = [years[i:i+4] for i in range(0, len(years), 4)]
    menu.append(["📅 كل السنوات", "⬅️ الرجوع", "🏠 الرئيسية"])
    return menu

def get_streams_menu(subject):
    return [[stream] for stream in subjects_with_streams.get(subject, [])] + [["⬅️ الرجوع", "🏠 الرئيسية"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text("مرحبًا بك! اختر أحد الخيارات التالية:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_data = context.user_data

    if text == "🏠 الرئيسية":
        user_data.clear()
        await update.message.reply_text("عدنا إلى القائمة الرئيسية.", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

    elif text == "⬅️ الرجوع":
        history = user_data.get("history", [])
        if history:
            last = history.pop()
            user_data["history"] = history
            if last == "المواد":
                await update.message.reply_text("اختر المادة:", reply_markup=ReplyKeyboardMarkup(get_subjects_menu(), resize_keyboard=True))
            elif last == "الأقسام":
                await update.message.reply_text("اختر القسم:", reply_markup=ReplyKeyboardMarkup(topics_menu, resize_keyboard=True))
            else:
                await update.message.reply_text("تم الرجوع.", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
        else:
            await update.message.reply_text("أنت في القائمة الرئيسية.", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

    elif text == "📘 الملخصات":
        user_data["section"] = "الملخصات"
        user_data["history"] = ["المواد"]
        await update.message.reply_text("اختر المادة:", reply_markup=ReplyKeyboardMarkup(get_subjects_menu(), resize_keyboard=True))

    elif text == "📚 المواضيع":
        user_data["section"] = "المواضيع"
        user_data["history"] = ["الأقسام"]
        await update.message.reply_text("اختر نوع المواضيع:", reply_markup=ReplyKeyboardMarkup(topics_menu, resize_keyboard=True))

    elif text == "📝 الباكالوريات":
        user_data["section"] = "الباكالوريات"
        user_data["history"] = ["المواد"]
        await update.message.reply_text("اختر المادة:", reply_markup=ReplyKeyboardMarkup(get_subjects_menu(), resize_keyboard=True))

    elif text in ["📕 الفصل الأول", "📘 الفصل الثاني", "📙 الفصل الثالث", "📔 شامل"]:
        user_data["topic_type"] = text
        user_data["history"].append("المواد")
        await update.message.reply_text("اختر المادة:", reply_markup=ReplyKeyboardMarkup(get_subjects_menu(), resize_keyboard=True))

    elif text in subjects_with_streams:
        user_data["subject"] = text
        streams = subjects_with_streams[text]
        if streams:
            user_data["history"].append("الشعبة")
            await update.message.reply_text("اختر الشعبة:", reply_markup=ReplyKeyboardMarkup(get_streams_menu(text), resize_keyboard=True))
        else:
            if user_data.get("section") == "الباكالوريات":
                user_data["history"].append("السنوات")
                await update.message.reply_text("اختر السنة:", reply_markup=ReplyKeyboardMarkup(get_years_menu(), resize_keyboard=True))
            else:
                await update.message.reply_text(f"📄 سيتم عرض المحتوى لاحقًا لـ {text}", reply_markup=ReplyKeyboardMarkup([["⬅️ الرجوع", "🏠 الرئيسية"]], resize_keyboard=True))

    elif text in sum([v for v in subjects_with_streams.values()], []):
        if user_data.get("section") == "الباكالوريات":
            user_data["stream"] = text
            user_data["history"].append("السنوات")
            await update.message.reply_text("اختر السنة:", reply_markup=ReplyKeyboardMarkup(get_years_menu(), resize_keyboard=True))
        else:
            await update.message.reply_text(f"📄 سيتم عرض المحتوى لاحقًا لـ {user_data.get('subject')} - {text}", reply_markup=ReplyKeyboardMarkup([["⬅️ الرجوع", "🏠 الرئيسية"]], resize_keyboard=True))

    elif text in [str(year) for year in range(2008, 2026)] + ["📅 كل السنوات"]:
        await update.message.reply_text(f"📄 سيتم عرض مواضيع {user_data.get('subject')} - {user_data.get('stream')} - {text} لاحقًا", reply_markup=ReplyKeyboardMarkup([["⬅️ الرجوع", "🏠 الرئيسية"]], resize_keyboard=True))

    else:
        await update.message.reply_text("يرجى اختيار خيار من القائمة.", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

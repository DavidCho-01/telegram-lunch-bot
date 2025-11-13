
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
import datetime

EMPLOYEES = ["홍길동", "김철수", "이영희", "최민수"]

daily_check = {name: False for name in EMPLOYEES}

def build_keyboard():
    keyboard = []
    for name in EMPLOYEES:
        mark = "☑" if daily_check[name] else "☐"
        keyboard.append([InlineKeyboardButton(f"{name} {mark}", callback_data=name)])

    keyboard.append([InlineKeyboardButton("결과 보기", callback_data="RESULT")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("오늘 점심 드실 분 체크해주세요.", reply_markup=build_keyboard())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "RESULT":
        today = datetime.date.today().strftime("%Y-%m-%d")
        selected = [name for name, checked in daily_check.items() if checked]
        count = len(selected)

        result_text = f"📅 {today} 점심 인원\n총 {count}명\n\n"
        if selected:
            result_text += "\n".join(f"- {name}" for name in selected)
        else:
            result_text += "선택된 사람이 없습니다."

        await query.edit_message_text(result_text)
    else:
        name = query.data
        daily_check[name] = not daily_check[name]
        await query.edit_message_reply_markup(reply_markup=build_keyboard())

TOKEN = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()


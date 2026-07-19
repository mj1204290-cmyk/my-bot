import telebot
from telebot import types
from flask import Flask
from threading import Thread

# আপনার বটের টোকেন
BOT_TOKEN = '8856215877:AAFpxVrNp0t43af9iKB7IE-fARFmuYaJZEE'
bot = telebot.TeleBot(BOT_TOKEN)

# আপনার পার্সোনাল ইমেইল এবং পাসওয়ার্ড
MY_EMAIL = "maisha3gh.com"
MY_PASS = "maisha3gh123"

user_state = {}

# --- লগইন সিস্টেম ---
@bot.message_handler(commands=['admin'])
def admin_login(message):
    bot.send_message(message.chat.id, "অ্যাডমিন প্যানেলে স্বাগতম! আপনার ইমেইলটি লিখুন:")
    user_state[message.chat.id] = {'step': 'email'}

@bot.message_handler(func=lambda m: m.chat.id in user_state or (m.chat.id in user_state and user_state[m.chat.id].get('step') == 'logged_in'))
def handle_steps(message):
    chat_id = message.chat.id
    state = user_state[chat_id].get('step')

    # লগইন প্রসেস
    if state == 'email':
        if message.text == MY_EMAIL:
            user_state[chat_id]['step'] = 'password'
            bot.send_message(chat_id, "ইমেইল সঠিক! এবার আপনার পাসওয়ার্ড দিন:")
        else:
            bot.send_message(chat_id, "ভুল ইমেইল! লগইন বাতিল।")
            del user_state[chat_id]

    elif state == 'password':
        if message.text == MY_PASS:
            user_state[chat_id]['step'] = 'logged_in'
            # অ্যাডমিন প্যানেলের বাটন
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("📊 ইউজার লিস্ট", "💰 উইথড্র রিকোয়েস্ট", "❌ লগআউট")
            bot.send_message(chat_id, "লগইন সফল! ✅ আপনি এখন অ্যাডমিন প্যানেলে আছেন।", reply_markup=markup)
        else:
            bot.send_message(chat_id, "ভুল পাসওয়ার্ড! লগইন বাতিল।")
            del user_state[chat_id]

    # লগইন হওয়ার পরের কাজ
    elif state == 'logged_in':
        if message.text == "📊 ইউজার লিস্ট":
            bot.send_message(chat_id, "বর্তমানে কোনো ইউজার ডাটা নেই।")
        elif message.text == "💰 উইথড্র রিকোয়েস্ট":
            bot.send_message(chat_id, "এখানে উইথড্র রিকোয়েস্টগুলো দেখা যাবে।")
        elif message.text == "❌ লগআউট":
            del user_state[chat_id]
            markup = types.ReplyKeyboardRemove()
            bot.send_message(chat_id, "লগআউট সফল! প্যানেল বন্ধ করা হয়েছে।", reply_markup=markup)

# --- Flask সার্ভার ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.polling(none_stop=True)

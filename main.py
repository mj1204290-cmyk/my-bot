from flask import Flask
from threading import Thread
import telebot
from telebot import types

# আপনার বটের টোকেন
BOT_TOKEN = 88562158:AAFpxVrNp0t43af9iKB7IE' + '-fARFmuYaJZEE''
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_EMAIL = "maisha3gh123.com"
ADMIN_PASS = "Maisha3gh"

user_state = {}

# ১. লগইন কমান্ড
@bot.message_handler(commands=['admin', 'panel'])
def start_login(message):
    bot.send_message(message.chat.id, "অ্যাডমিন প্যানেলে স্বাগতম। ইমেইল দিন:")
    user_state[message.chat.id] = {'step': 'ask_email'}

# ২. লগইন প্রসেস
@bot.message_handler(func=lambda message: message.chat.id in user_state)
def handle_login(message):
    chat_id = message.chat.id
    state = user_state[chat_id].get('step')
    
    if state == 'ask_email':
        if message.text == ADMIN_EMAIL:
            user_state[chat_id]['step'] = 'ask_pass'
            bot.send_message(chat_id, "ইমেইল সঠিক। পাসওয়ার্ড দিন:")
        else:
            bot.send_message(chat_id, "ভুল ইমেইল! অপারেশন বাতিল।")
            del user_state[chat_id]
            
    elif state == 'ask_pass':
        if message.text == ADMIN_PASS:
            user_state[chat_id]['step'] = 'logged_in'
            show_admin_panel(chat_id)
        else:
            bot.send_message(chat_id, "ভুল পাসওয়ার্ড! লগইন বাতিল।")
            del user_state[chat_id]
    
    elif state == 'logged_in':
        admin_actions(message)

# ৩. প্যানেল দেখানোর ফাংশন
def show_admin_panel(chat_id):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("📊 ইউজার লিস্ট", "💰 উইথড্র রিকোয়েস্ট", "❌ লগআউট")
    bot.send_message(chat_id, "✅ লগইন সফল! আপনি এখন অ্যাডমিন মোডে আছেন।", reply_markup=markup)

# ৪. প্যানেলের বাটনগুলোর কাজ
def admin_actions(message):
    if message.text == "📊 ইউজার লিস্ট":
        bot.send_message(message.chat.id, "এখানে ইউজার লিস্ট দেখাবে...")
    elif message.text == "💰 উইথড্র রিকোয়েস্ট":
        bot.send_message(message.chat.id, "এখানে উইথড্র রিকোয়েস্ট দেখাবে...")
    elif message.text == "❌ লগআউট":
        user_state[message.chat.id]['step'] = 'logged_out'
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "লগআউট সফল! প্যানেল হাইড করা হয়েছে।", reply_markup=markup)
        del user_state[message.chat.id]

# Flask সার্ভার চালু করা (রেন্ডারের জন্য)
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)

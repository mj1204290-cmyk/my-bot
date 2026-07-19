import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os

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

@bot.message_handler(func=lambda m: m.chat.id in user_state)
def handle_steps(message):
    chat_id = message.chat.id
    state = user_state[chat_id].get('step')

    if state == 'email':
        if message.text == MY_EMAIL:
            user_state[chat_id]['step'] = 'password'
            bot.send_message(chat_id, "ইমেইল সঠিক! এবার আপনার পাসওয়ার্ড দিন:")
        else:
            bot.send_message(chat_id, "ভুল ইমেইল! লগইন বাতিল।")
            del user_state[chat_id]

    elif state == 'password':
        if message.text == MY_PASS:
            bot.send_message(chat_id, "লগইন সফল! ✅ আপনি এখন অ্যাডমিন প্যানেলে আছেন।")
            user_state[chat_id]['step'] = 'logged_in'
        else:
            bot.send_message(chat_id, "ভুল পাসওয়ার্ড! লগইন বাতিল।")
            del user_state[chat_id]

# --- Flask সার্ভার (রেন্ডারের জন্য বাধ্যতামূলক) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # সার্ভারটি ব্যাকগ্রাউন্ডে চালু করা
    Thread(target=run_server).start()
    # বট পোলিং চালু করা
    bot.polling(none_stop=True)

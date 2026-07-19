import telebot
from telebot import types

# আপনার বটের টোকেন
BOT_TOKEN = '8856215877:AAFpxVrNp0t43af9iKB7IE-fARFmuYaJZEE'
bot = telebot.TeleBot(BOT_TOKEN)

# আপনার পার্সোনাল ইমেইল এবং পাসওয়ার্ড
MY_EMAIL = "maisha3gh.com"  # এখানে আপনার ইমেইল দিন
MY_PASS = "maisha3gh123"     # এখানে আপনার গোপন পাসওয়ার্ড দিন

# ইউজারদের স্ট্যাটাস ট্র্যাক করার জন্য
user_state = {}

@bot.message_handler(commands=['admin'])
def admin_login(message):
    bot.send_message(message.chat.id, "অ্যাডমিন প্যানেলে স্বাগতম! আপনার ইমেইলটি লিখুন:")
    user_state[message.chat.id] = {'step': 'email'}

@bot.message_handler(func=lambda m: m.chat.id in user_state)
def handle_steps(message):
    chat_id = message.chat.id
    state = user_state[chat_id]['step']

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
            # এখানে প্যানেলের বাটনগুলো দেখান
        else:
            bot.send_message(chat_id, "ভুল পাসওয়ার্ড! লগইন বাতিল।")
            del user_state[chat_id]

import telebot
from telebot import types
from flask import Flask
from threading import Thread

# আপনার বটের টোকেন
BOT_TOKEN = '8856215877:AAFpxVrNp0t43af9iKB7IE-fARFmuYaJZEE'
bot = telebot.TeleBot(BOT_TOKEN)

# আপনার ইমেইল এবং পাসওয়ার্ড
MY_EMAIL = "maisha3gh.com"
MY_PASS = "maisha3gh123"

# ডাটা স্টোরেজ
user_state = {}
user_list = {} 
withdraw_requests = []

# --- ইউজার কমান্ডস ---
@bot.message_handler(commands=['start'])
def start(message):
    user_list[message.chat.id] = message.from_user.first_name
    bot.reply_to(message, "স্বাগতম! কাজ শুরু করতে /withdraw কমান্ড দিন।")

@bot.message_handler(commands=['withdraw'])
def withdraw_start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("বিকাশ", "নগদ")
    bot.reply_to(message, "পেমেন্ট মেথড সিলেক্ট করুন:", reply_markup=markup)
    user_state[message.chat.id] = {'step': 'select_method'}

# --- অ্যাডমিন এবং ইন্টারঅ্যাকশন হ্যান্ডলার ---
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    chat_id = message.chat.id
    
    # উইথড্র ফ্লো (ইউজার)
    if chat_id in user_state and user_state[chat_id].get('step') == 'select_method':
        user_state[chat_id]['method'] = message.text
        user_state[chat_id]['step'] = 'enter_amount'
        bot.reply_to(message, f"{message.text} সিলেক্ট করেছেন। কত টাকা উইথড্র করবেন লিখুন:")
        return

    if chat_id in user_state and user_state[chat_id].get('step') == 'enter_amount':
        method = user_state[chat_id]['method']
        withdraw_requests.append(f"👤 {message.from_user.first_name} | মেথড: {method} | টাকা: {message.text}")
        bot.reply_to(message, "আপনার উইথড্র রিকোয়েস্টটি অ্যাডমিনের কাছে পাঠানো হয়েছে।")
        del user_state[chat_id]
        return

    # লগইন ফ্লো (অ্যাডমিন)
    if message.text == '/admin':
        bot.send_message(chat_id, "অ্যাডমিন প্যানেলে স্বাগতম! ইমেইল দিন:")
        user_state[chat_id] = {'step': 'email'}
        return

    if chat_id in user_state:
        state = user_state[chat_id].get('step')
        
        if state == 'email':
            if message.text == MY_EMAIL:
                user_state[chat_id]['step'] = 'password'
                bot.send_message(chat_id, "ইমেইল সঠিক! পাসওয়ার্ড দিন:")
            else:
                bot.send_message(chat_id, "ভুল ইমেইল! লগইন বাতিল।"); del user_state[chat_id]
        
        elif state == 'password':
            if message.text == MY_PASS:
                user_state[chat_id]['step'] = 'logged_in'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("📊 ইউজার লিস্ট", "💰 উইথড্র রিকোয়েস্ট", "❌ লগআউট")
                bot.send_message(chat_id, "লগইন সফল! ✅", reply_markup=markup)
            else:
                bot.send_message(chat_id, "ভুল পাসওয়ার্ড! লগইন বাতিল।"); del user_state[chat_id]
        
        elif state == 'logged_in':
            if message.text == "📊 ইউজার লিস্ট":
                msg = "ইউজার তালিকা:\n" + "\n".join([f"- {name}" for name in user_list.values()])
                bot.send_message(chat_id, msg if user_list else "কেউ নেই")
            elif message.text == "💰 উইথড্র রিকোয়েস্ট":
                msg = "উইথড্র রিকোয়েস্ট:\n" + "\n".join(withdraw_requests)
                bot.send_message(chat_id, msg if withdraw_requests else "কোনো রিকোয়েস্ট নেই")
            elif message.text == "❌ লগআউট":
                del user_state[chat_id]
                bot.send_message(chat_id, "লগআউট সফল!", reply_markup=types.ReplyKeyboardRemove())

# --- Flask সার্ভার ---
app = Flask('')
@app.route('/')
def home(): return "Bot is running!"

def run_server(): app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.polling(none_stop=True)

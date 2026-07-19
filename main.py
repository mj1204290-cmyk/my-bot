import telebot
from telebot import types
from flask import Flask
from threading import Thread

# বটের টোকেন
BOT_TOKEN = '8856215877:AAFpxVrNp0t43af9iKB7IE-fARFmuYaJZEE'
bot = telebot.TeleBot(BOT_TOKEN)

# অ্যাডমিন ক্রেডেন্সিয়ালস
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
    bot.reply_to(message, "স্বাগতম! উইথড্র দিতে /withdraw কমান্ড দিন।")

@bot.message_handler(commands=['withdraw'])
def withdraw_start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("বিকাশ", "নগদ")
    bot.reply_to(message, "পেমেন্ট মেথড সিলেক্ট করুন:", reply_markup=markup)
    user_state[message.chat.id] = {'step': 'select_method'}

# --- মেইন হ্যান্ডলার ---
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    chat_id = message.chat.id
    
    # ১. উইথড্র প্রসেস (ইউজার)
    if chat_id in user_state and user_state[chat_id].get('step') == 'select_method':
        user_state[chat_id]['method'] = message.text
        user_state[chat_id]['step'] = 'enter_details'
        bot.reply_to(message, f"{message.text} সিলেক্ট করেছেন। আপনার টাকার পরিমাণ এবং নাম্বার একসাথে লিখুন (যেমন: 500 017xxxxxxxx):")
        return

    if chat_id in user_state and user_state[chat_id].get('step') == 'enter_details':
        method = user_state[chat_id]['method']
        withdraw_requests.append(f"👤 {message.from_user.first_name} | মেথড: {method} | তথ্য: {message.text}")
        bot.reply_to(message, "আপনার রিকোয়েস্টটি জমা হয়েছে। অ্যাডমিন চেক করে পেমেন্ট করে দেবেন।")
        del user_state[chat_id]
        return

    # ২. অ্যাডমিন লগইন প্রসেস
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
                bot.send_message(chat_id, "ভুল ইমেইল!"); del user_state[chat_id]
        
        elif state == 'password':
            if message.text == MY_PASS:
                user_state[chat_id]['step'] = 'logged_in'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("📊 ইউজার লিস্ট", "💰 উইথড্র রিকোয়েস্ট", "❌ লগআউট")
                bot.send_message(chat_id, "লগইন সফল! ✅", reply_markup=markup)
            else:
                bot.send_message(chat_id, "ভুল পাসওয়ার্ড!"); del user_state[chat_id]
        
        # ৩. অ্যাডমিন প্যানেল অ্যাকশন
        elif state == 'logged_in':
            if message.text == "📊 ইউজার লিস্ট":
                msg = "ইউজার তালিকা:\n" + ("\n".join([f"- {name}" for name in user_list.values()]) if user_list else "কেউ নেই")
                bot.send_message(chat_id, msg)
            
            elif message.text == "💰 উইথড্র রিকোয়েস্ট":
                if not withdraw_requests:
                    bot.send_message(chat_id, "কোনো রিকোয়েস্ট নেই।")
                else:
                    for i, req in enumerate(withdraw_requests):
                        markup = types.InlineKeyboardMarkup()
                        paid_btn = types.InlineKeyboardButton("✅ পেমেন্ট সম্পন্ন (Paid)", callback_data=f"paid_{i}")
                        markup.add(paid_btn)
                        bot.send_message(chat_id, f"রিকোয়েস্ট #{i+1}:\n{req}", reply_markup=markup)
            
            elif message.text == "❌ লগআউট":
                del user_state[chat_id]
                bot.send_message(chat_id, "লগআউট সফল!", reply_markup=types.ReplyKeyboardRemove())

# --- পেমেন্ট এপ্রুভ হ্যান্ডলার ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('paid_'))
def handle_paid(call):
    index = int(call.data.split('_')[1])
    if index < len(withdraw_requests):
        req_data = withdraw_requests[index]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=f"✅ পেমেন্ট সম্পন্ন করা হয়েছে:\n{req_data}")
        bot.answer_callback_query(call.id, "সফলভাবে মার্ক করা হয়েছে!")
    else:
        bot.answer_callback_query(call.id, "এটি ইতিমধ্যে মার্ক করা হয়েছে।")

# --- সার্ভার ---
app = Flask('')
@app.route('/')
def home(): return "Bot is running!"

def run_server(): app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    Thread(target=run_server).start()
    bot.polling(none_stop=True)

from pyrogram import Client, filters
import os, json

# Pyrogram client তৈরি
app = Client(
    "forwarder",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# ইউজারদের সোর্স ও ডেস্টিনেশন সংরক্ষণ করার জন্য কনফিগ ফাইল
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

config = load_config()

@app.on_message(filters.command("start") & filters.private)
def start(client, message):
    message.reply(
        "👋 স্বাগতম!\n\n/set_source ও /set_destination কমান্ড দিয়ে সোর্স ও ডেস্টিনেশন চ্যানেল সেট করুন।\n\nউদাহরণ:\n`/set_source -1001234567890`\n`/set_destination -1009876543210`",
        quote=True
    )

@app.on_message(filters.command("set_source") & filters.private)
def set_source(client, message):
    user_id = str(message.from_user.id)
    if len(message.command) < 2:
        message.reply("❌ সোর্স চ্যাট আইডি দিতে ভুলে গেছেন।\nউদাহরণ: `/set_source -1001234567890`", quote=True)
        return
    chat_id = message.command[1]
    config[user_id] = config.get(user_id, {})
    config[user_id]["source"] = chat_id
    save_config(config)
    message.reply(f"✅ Source chat ID সেট হয়েছে: `{chat_id}`", quote=True)

@app.on_message(filters.command("set_destination") & filters.private)
def set_destination(client, message):
    user_id = str(message.from_user.id)
    if len(message.command) < 2:
        message.reply("❌ ডেস্টিনেশন চ্যাট আইডি দিতে ভুলে গেছেন।\nউদাহরণ: `/set_destination -1009876543210`", quote=True)
        return
    chat_id = message.command[1]
    config[user_id] = config.get(user_id, {})
    config[user_id]["destination"] = chat_id
    save_config(config)
    message.reply(f"✅ Destination chat ID সেট হয়েছে: `{chat_id}`", quote=True)

@app.on_message()
def auto_forward(client, message):
    user_id = str(message.from_user.id)
    if user_id in config and "source" in config[user_id] and "destination" in config[user_id]:
        if str(message.chat.id) == config[user_id]["source"]:
            dest = int(config[user_id]["destination"])
            client.copy_message(chat_id=dest, from_chat_id=message.chat.id, message_id=message.id)

app.run()

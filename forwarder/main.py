import os
import json
from pyrogram import Client, filters

# ==========================
# Config / Environment
# ==========================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

CONFIG_FILE = "chat_list.json"

# ==========================
# Auto-create config file
# ==========================
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump({}, f)

# ==========================
# Load / Save Functions
# ==========================
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

config = load_config()

# ==========================
# Initialize Pyrogram Client
# ==========================
app = Client("forwarder", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ==========================
# Command Handlers
# ==========================
@app.on_message(filters.command("start") & filters.private)
def start(client, message):
    message.reply(
        "👋 স্বাগতম!\n\n"
        "সোর্স এবং ডেস্টিনেশন চ্যানেল/গ্রুপ সেট করতে:\n"
        "`/set_source <chat_id>`\n"
        "`/set_destination <chat_id>`",
        quote=True
    )

@app.on_message(filters.command("set_source") & filters.private)
def set_source(client, message):
    user_id = str(message.from_user.id)
    if len(message.command) < 2:
        message.reply("❌ সোর্স চ্যাট আইডি দিতে ভুলেছেন। উদাহরণ: `/set_source -1001234567890`", quote=True)
        return
    chat_id = message.command[1]
    config[user_id] = config.get(user_id, {})
    config[user_id]["source"] = chat_id
    save_config(config)
    message.reply(f"✅ Source chat ID set: `{chat_id}`", quote=True)

@app.on_message(filters.command("set_destination") & filters.private)
def set_destination(client, message):
    user_id = str(message.from_user.id)
    if len(message.command) < 2:
        message.reply("❌ ডেস্টিনেশন চ্যাট আইডি দিতে ভুলেছেন। উদাহরণ: `/set_destination -1009876543210`", quote=True)
        return
    chat_id = message.command[1]
    config[user_id] = config.get(user_id, {})
    config[user_id]["destination"] = chat_id
    save_config(config)
    message.reply(f"✅ Destination chat ID set: `{chat_id}`", quote=True)

# ==========================
# Auto-forward Handler
# ==========================
@app.on_message()
def auto_forward(client, message):
    user_id = str(message.from_user.id)
    if user_id in config:
        user_config = config[user_id]
        if "source" in user_config and "destination" in user_config:
            if str(message.chat.id) == user_config["source"]:
                dest = int(user_config["destination"])
                client.copy_message(chat_id=dest, from_chat_id=message.chat.id, message_id=message.id)

# ==========================
# Run Bot
# ==========================
app.run()

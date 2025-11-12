from flask import Flask
import threading
import time
import logging
from telethon import TelegramClient, events

# ================= TELEGRAM CONFIG =================
api_id = 38317834
api_hash = '9b9b9cd5c632a01e00d6b27857eb2c1f'

# Source and target channels
# Use usernames if possible. For private channels, the account must already be joined
source_channels = [
    'EasyForexPips',       # public channel username
    '+0UaKPqnhXbg2Yjhl',  # private channel invite hash
    '+HBAsg_1cXoYzYjFl'
]
target_channel = '+WB5EH_NEcKMrOxmL'  # your target channel invite hash

# Session file
session_file = 'auto_forward_session'

client = TelegramClient(session_file, api_id, api_hash)

# ================= LOGGING =================
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================= FLASK SERVER =================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# ================= TELEGRAM BOT =================
async def get_chat_id(link):
    try:
        entity = await client.get_entity(link)
        logging.info(f"✅ {link} → ID: {entity.id}")
        return entity.id
    except Exception as e:
        logging.error(f"⚠️ Failed to get ID for {link}: {e}")
        return None

async def main():
    # Start the client session (will prompt for login on first run)
    await client.start()
    logging.info("✅ Client started")

    # Get chat IDs
    logging.info("🔍 Resolving channel IDs...")
    src_ids = []
    for link in source_channels:
        chat_id = await get_chat_id(link)
        if chat_id:
            src_ids.append(chat_id)

    dest_id = await get_chat_id(target_channel)

    logging.info("🎯 Listening to channels...")

    @client.on(events.NewMessage(chats=src_ids))
    async def handler(event):
        try:
            await client.forward_messages(dest_id, event.message)
            logging.info(f"➡️ Forwarded from {event.chat.title}: {event.message.id}")
        except Exception as e:
            logging.error(f"⚠️ Error forwarding: {e}")

    logging.info("✅ Bot ready! Waiting for messages...")
    await client.run_until_disconnected()

# ================= AUTO-RECONNECT LOOP =================
def start_bot():
    while True:
        try:
            with client:
                client.loop.run_until_complete(main())
        except Exception as e:
            logging.error(f"⚠️ Bot crashed: {e}")
            logging.info("⏳ Restarting in 5 seconds...")
            time.sleep(5)

# Start bot in a separate thread
threading.Thread(target=start_bot).start()

# ================= RUN FLASK SERVER =================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

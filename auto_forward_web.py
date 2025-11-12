from flask import Flask
import threading
from telethon import TelegramClient, events

# === TELEGRAM API INFO ===
api_id = 38317834
api_hash = '9b9b9cd5c632a01e00d6b27857eb2c1f'

# === CHANNEL LINKS ===
source_channels = [
    'https://t.me/EasyForexPips',
    'https://t.me/+0UaKPqnhXbg2Yjhl',
]
target_channel = 'https://t.me/+WB5EH_NEcKMrOxmL'

# === TELETHON CLIENT ===
client = TelegramClient('auto_forward_session', api_id, api_hash)

# === FLASK SERVER ===
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# === TELEGRAM BOT LOGIC ===
async def get_chat_id(link):
    try:
        entity = await client.get_entity(link)
        print(f"✅ {link} → ID: {entity.id}")
        return entity.id
    except Exception as e:
        print(f"⚠️ Failed to get ID for {link}: {e}")
        return None

async def main():
    print("\n🔍 Getting channel IDs...")
    src_ids = []
    for link in source_channels:
        chat_id = await get_chat_id(link)
        if chat_id:
            src_ids.append(chat_id)

    dest_id = await get_chat_id(target_channel)
    print("\n🎯 Listening to channels...\n")

    @client.on(events.NewMessage(chats=src_ids))
    async def handler(event):
        try:
            await client.forward_messages(dest_id, event.message)
            print(f"➡️ Forwarded from {event.chat.title}")
        except Exception as e:
            print(f"⚠️ Error forwarding: {e}")

    print("✅ Ready! Waiting for new messages...")
    await client.run_until_disconnected()

# === RUN TELEGRAM BOT IN THREAD ===
def start_bot():
    with client:
        client.loop.run_until_complete(main())

threading.Thread(target=start_bot).start()

# === RUN FLASK SERVER (Render requires binding to a port) ===
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

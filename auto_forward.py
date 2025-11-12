from telethon import TelegramClient, events

# === STEP 1: FILL YOUR TELEGRAM API INFO ===
api_id = 38317834  # <<-- your API ID
api_hash = '9b9b9cd5c632a01e00d6b27857eb2c1f'  # <<-- your API hash

# === STEP 2: FILL CHANNEL LINKS ===
source_channels = [
    'https://t.me/EasyForexPips',      # <<-- channel 1
    'https://t.me/+0UaKPqnhXbg2Yjhl',  # <<-- channel 2 (private or public)
]
target_channel = 'https://t.me/+WB5EH_NEcKMrOxmL'  # <<-- your own channel

# ==========================================================
# YOU DON'T NEED TO EDIT BELOW THIS LINE (unless advanced)
# ==========================================================

client = TelegramClient('auto_forward_session', api_id, api_hash)

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

with client:
    client.loop.run_until_complete(main())

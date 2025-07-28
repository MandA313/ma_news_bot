import os
import asyncio
from telethon import TelegramClient, events

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
owner_id = int(os.getenv("OWNER_ID"))
source_channels = os.getenv("SOURCE_CHANNELS").split(",")
target_channel = os.getenv("TARGET_CHANNEL")

client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)
translator = Translator()

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        msg = event.message
        original_text = msg.text or msg.message or ""
        translated_text = ""
        if original_text:
            try:
                translated_text = translator.translate(original_text, dest="ru").text
            except:
                translated_text = original_text

        if msg.media:
            await client.send_file(target_channel, file=msg.media, caption=translated_text)
        else:
            await client.send_message(target_channel, translated_text)

        preview = translated_text[:200].replace("\n", " ")
        log_msg = f"✅ Новость опубликована\n📡 Источник: {event.chat.username or 'private'}\n🕒 Время: {msg.date.strftime('%Y-%m-%d %H:%M')}\n📜 Текст: {preview}"
        await client.send_message(owner_id, log_msg)

    except Exception as e:
        await client.send_message(owner_id, f"❌ Ошибка публикации: {str(e)}")

client.run_until_disconnected()

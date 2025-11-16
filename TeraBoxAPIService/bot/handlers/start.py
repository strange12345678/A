from pyrogram import filters
from pyrogram.types import Message
from TeraBoxAPIService.bot.utils.database import Database
from TeraBoxAPIService.config import settings


async def handle_start(client, message: Message):
    db = Database()
    db.connect()
    user_id = message.from_user.id
    # create user if missing and issue trial if no key
    user = await db.get_user(user_id)
    if not user or not user.get("api_key"):
        trial = await db.create_trial_key(user_id)
        api_endpoint = f"{settings.API_URL}/run"
        text = (
            f"🎉 Your trial API key: `{trial['key']}`\n"
            f"Expiry: {trial['expiry'].isoformat()}\n"
            f"Usage limit: {trial['max_usage']}\n\n"
            f"Use it with:\n"
            f"`{api_endpoint}?key={trial['key']}&url=TERABOX_LINK`"
        )
        await message.reply_text(text)
        return

    # show existing key
    api_endpoint = f"{settings.API_URL}/run"
    text = (
        f"Your API key: `{user['api_key']}`\n"
        f"Plan: {user.get('plan')}\n"
        f"Expiry: {user.get('expiry')}\n"
        f"Usage: {user.get('usage_count',0)}/{user.get('max_usage',0)}\n\n"
        f"API Endpoint:\n"
        f"`{api_endpoint}?key={user['api_key']}&url=TERABOX_LINK`"
    )
    await message.reply_text(text)

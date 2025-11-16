"""
Web wrapper for Telegram bot - allows bot to run on Render as a web service
instead of just a background process.
"""
import asyncio
import threading
from fastapi import FastAPI
from pyrogram import Client
from TeraBoxAPIService.config import settings
from TeraBoxAPIService.bot.handlers import start as start_h
from TeraBoxAPIService.bot.handlers import keys as keys_h
from TeraBoxAPIService.bot.handlers import admin as admin_h
from pyrogram import filters

app = FastAPI(title="TeraBox Bot Service")
bot_client = None


@app.get("/")
async def health_check():
    """Health check endpoint for Render"""
    return {"status": "ok", "service": "TeraBox Bot", "version": "1.0"}


@app.get("/health")
async def health():
    """Alternative health check"""
    return {"status": "running", "bot": "active" if bot_client and bot_client.is_connected else "starting"}


def setup_bot():
    """Initialize and setup bot handlers"""
    global bot_client
    bot_client = Client(
        "terabox_bot",
        bot_token=settings.BOT_TOKEN,
        api_id=settings.API_ID,
        api_hash=settings.API_HASH
    )

    # Register handlers
    @bot_client.on_message(filters.command("start"))
    async def _start(client, message):
        await start_h.handle_start(client, message)

    @bot_client.on_message(filters.command("mykey"))
    async def _mykey(client, message):
        await keys_h.handle_mykey(client, message)

    @bot_client.on_message(filters.command("help"))
    async def _help(client, message):
        await keys_h.handle_help(client, message)

    @bot_client.on_message(filters.command("addpremium"))
    async def _addpremium(client, message):
        await admin_h.cmd_addpremium(client, message)

    @bot_client.on_message(filters.command("extend"))
    async def _extend(client, message):
        await admin_h.cmd_extend(client, message)

    @bot_client.on_message(filters.command("remove"))
    async def _remove(client, message):
        await admin_h.cmd_remove(client, message)

    @bot_client.on_message(filters.command("ban"))
    async def _ban(client, message):
        await admin_h.cmd_ban(client, message)

    @bot_client.on_message(filters.command("unban"))
    async def _unban(client, message):
        await admin_h.cmd_unban(client, message)

    @bot_client.on_message(filters.command("allkeys"))
    async def _allkeys(client, message):
        await admin_h.cmd_allkeys(client, message)

    @bot_client.on_message(filters.command("userinfo"))
    async def _userinfo(client, message):
        await admin_h.cmd_userinfo(client, message)

    print("🤖 Bot handlers registered")
    return bot_client


def run_bot_in_thread():
    """Run bot in a separate thread with its own event loop"""
    def bot_thread_main():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            client = setup_bot()
            print("🤖 Starting bot...")
            client.run()
        except Exception as e:
            print(f"❌ Bot error: {e}")
        finally:
            loop.close()
    
    bot_thread = threading.Thread(target=bot_thread_main, daemon=True)
    bot_thread.start()
    return bot_thread


# Start bot in background when server starts
@app.on_event("startup")
async def startup_event():
    run_bot_in_thread()
    print("✅ Bot service started")


@app.on_event("shutdown")
async def shutdown_event():
    global bot_client
    if bot_client and bot_client.is_connected:
        bot_client.stop()
    print("🤖 Bot shutting down")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


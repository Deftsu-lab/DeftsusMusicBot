from pathlib import Path

import discord
from discord.ext import commands


class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix,
                         case_insensitive=True,
                         intents=discord.Intents.all())

    def setup(self):
        print("Piano stimmt sich...")

        for Cog in self._cogs:
            self.load_extension(f"bot.cogs.{Cog}")
            print(f"'{Cog}' cog geladen")

        print("Piano gestimmt")

    def run(self):
        self.setup()

        with open("data/token.0", "r", encoding="utf-8") as f:
            TOKEN = f.read()

        print("Wird hochetragen...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Verbindung wird unterbrochen...")
        await super().close()

    async def close(self):
        print("Schließt on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f"Connected (ping: {self.latency*1000:,.0f} ms).")

    async def on_resume(self):
        print("bot resumed")

    async def on_disconnect(self):
        print("Disconnected")

    async def on_error(self, err, *args, **kwargs):
        raise

    async def on_command_error(self, ctx, exc):
        raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bin endlich oben")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or(">")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)

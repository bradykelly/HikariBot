from __future__ import annotations
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from hikari.intents import Intents
from pytz import utc
from hikari_bot.bot import __version__
import logging
import hikari
import lightbulb


class Bot(lightbulb.Bot):
    def __init__(self) -> None:
        self._plugins = [p.stem for p in Path(".").glob("./testbot/bot/extensions/*.py")]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone="UTC")

        with open("./secrets/token", mode="r", encoding="utf-8") as f:
            token = f.read()

        super().__init__(
            prefix="-", 
            insensitive_commands=True,
            token=token,
            intents = Intents.ALL,
        )

    def run(self) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_stopped)   
        self.event_manager.subscribe(hikari.ExceptionEvent, self.on_exception) 
        self.event_manager.subscribe(hikari.MessageCreateEvent, self.on_message_create)    

        super().run(
            activity=hikari.Activity(
                name=f"-help | Version {__version__}", 
                type=hikari.ActivityType.WATCHING
            ),             
        )

    async def on_starting(self, event: hikari.StartingEvent) -> None:
        for ext in self.extensions:
            self.load_extension(f"testbot.extensions.{ext}")
            logging.info(f"Loaded extension {ext}")

    async def on_started(self, event: hikari.StartedEvent) -> None:
        self.scheduler.start()
        logging.info("Bot started")

    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        logging.info("Bot stopping")
        self.scheduler.shutdown()

    async def on_stopped(self, event: hikari.StoppedEvent) -> None:
        logging.info("Bot stopped")

    async def on_exception(self, event: hikari.ExceptionEvent) -> None:
        pass

    async def on_message_create(self, event: hikari.MessageCreateEvent) -> None:
        if event.message.member.is_bot or isinstance(event.message.channel_id, hikari.DMChannel):
            return

        logging.info(f"Message by {event.message.author}: {event.message.content}")
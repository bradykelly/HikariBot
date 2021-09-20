from hikari_bot.bot.bot import Bot
import hikari
import lightbulb


class Meta(lightbulb.Plugin):
    @lightbulb.command(name="ping")
    async def ping(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(f"Latency {ctx.bot.heartbeat_latency * 1_000:,.0f} ms")


def load(bot: Bot) -> None:
    bot.add_plugin(Meta())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Meta")
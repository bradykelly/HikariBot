from hikari_bot.bot.bot import Bot
import lightbulb


class Admin(lightbulb.Plugin):
    @lightbulb.owner_only()
    @lightbulb.command(name="shutdown", aliases=("sd",))
    async def shutdown(self, ctx: lightbulb.Context) -> None:
        await ctx.bot.close()


def load(bot: Bot) -> None:
    bot.add_plugin(Admin())

def unload(bot: Bot) -> None:
    bot.remove_plugin("Admin")        


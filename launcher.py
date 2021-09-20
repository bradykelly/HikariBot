from hikari_bot.bot import __version__
from hikari_bot.bot.bot import Bot
import os

if os.name != 'nt':
    import uvloop   
    uvloop.install()

if __name__ == '__main__':
    bot = Bot()
    bot.run()
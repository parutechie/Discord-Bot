import nextcord
from nextcord.ext import commands
from config import *


intents = nextcord.Intents.all()
intents.voice_states = True
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game('/'))
    print('BOT IS READY ✔')


# Load cogs
bot.load_extension('cogs.music')
bot.load_extension('cogs.welcome')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument.")
        print(error)
    else:
        await ctx.send("An error occurred while processing your request.")
        print(error)


bot.run(TOKEN)

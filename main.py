import discord
from discord.ext import commands
import json
import telepot
import os

bot = commands.Bot(command_prefix = "dtt!", case_insensitive = True)
bot.load_extension("jishaku")
t_bot = telepot.Bot("1265121590:AAEV3NkbIl6hoARwH4ONUQ3_mkzCuqPJeqA")
bot.remove_command("help")

async def to_discord(bot, channel_id: int, message, username):
    emb = discord.Embed(description = message, colour = discord.Colour.blurple())
    emb.set_author(name = username)
    channel = bot.get_channel(channel_id)
    await channel.send(embed = emb)

@bot.event
async def on_ready():
    print("ready as", bot.user)

@bot.event
async def on_message(message):

    await bot.process_commands(message)

    if message.author == bot.user:
        return

    with open("config.json", "r") as f:
        l = json.load(f)

    if str(message.guild.id) not in l:
        return

    if message.channel.id != l[str(message.guild.id)]["discord"]:
        return

    text = f"""*{message.author.display_name}*: {message.content}"""

    t_bot.sendMessage(l[str(message.guild.id)]["telegram"], text, parse_mode = 'Markdown')

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_type == "group" or chat_type == "supergroup":

        try:
            if msg["text"] == "/id" or msg["text"] == "/id@DiscordMessagesBot":
                return t_bot.sendMessage(chat_id, msg["chat"]["id"])
        except KeyError:
            return

        with open("config.json", "r") as f:
            l = json.load(f)

        for a in l:
            if l[a]["telegram"] == int(msg["chat"]["id"]):
                channel = int(l[a]["discord"])

        text = msg['text']

        if content_type == 'text':
            try:
                bot.loop.create_task(to_discord(bot, channel, text, msg["from"]["username"]))
            except KeyError:
                pass

@bot.command(aliases = ["setup"])
@commands.has_permissions(manage_messages = True)
async def config(ctx, telegram_id: int, *, channel: discord.TextChannel):
    "Setup the bot, type the telegram group id and tag the discord channel."

    with open("config.json", "r") as f:
        l = json.load(f)

    l[str(ctx.guild.id)] = {"telegram": telegram_id, "discord": channel.id}

    with open("config.json", "w") as f:
        json.dump(l, f, indent = 4)

    await ctx.send("Done!")

@bot.command()
async def invite(ctx):
    "Invite the bot to your server"

    emb = discord.Embed(title = "Invite me", url = discord.utils.oauth_url(bot.user.id, permissions = discord.Permissions(permissions=92160)), colour = discord.Colour.blurple())
    await ctx.send(embed = emb)

#@bot.event
#async def on_command_error(ctx, error):

#    if isinstance(error, commands.CommandNotFound):
 #       return
#
 #   emb = discord.Embed(title = "Error!", description = f"```css\n{error}\n```", colour = discord.Colour.red())
  #  await ctx.send(embed = emb)

t_bot.message_loop(on_chat_message)

for a in os.listdir("./cogs"):
    if a.endswith(".py"):
        bot.load_extension(f"cogs.{a[:-3]}")
    
bot.run("NzA2NTE3MzcxOTI5NzU1NjQ4.Xq7ZmQ.vyG7o_0db2GAEt7UHr74lwii13g")

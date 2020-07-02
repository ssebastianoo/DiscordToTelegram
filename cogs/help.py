import discord
from discord.ext import commands 

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True)
    async def help(self, ctx, *, command = None):
        emb = discord.Embed(title = "Help", colour = discord.Colour.blurple(), timestamp = ctx.message.created_at)
        emb.set_thumbnail(url = self.bot.user.avatar_url)
        error = discord.Embed(colour = discord.Color.red())

        if not command:

            res = ""
            for a in self.bot.commands:
              if not a.hidden:

                if a.name != "jishaku":

                    res += f"`{a.name} {a.signature}`\n"

                    try:
                    
                        for b in a.commands:

                            res += f"`{a.name} {b.name} {b.signature}`\n"

                    except:

                        pass

            emb.description = res
            return await ctx.send(embed = emb)

        else:

            a = self.bot.get_command(command)

            if not a:
                error.description = f"Command \"{command}\" not found!"
                return await ctx.send(embed = error)

            if a.parent:
                emb.add_field(value = f'**`{a.parent} {a.name} {a.signature}`**`', name = a.help, inline = False)
            else:
                emb.add_field(value = f'**`{a.name} {a.signature}`**', name = a.help, inline = False)

            if a.aliases:

                aliases = ""

                for a in a.aliases:

                    aliases += f"\n`{a}`"
                
                emb.add_field(name = 'Aliases', value = aliases, inline = False)

            try:
                commands = ""
            
                for b in a.commands:
                    commands += f"`{a.name} {b.name} {b.signature}`\n"
                
                emb.add_field(name = "Subcommands", value = commands, inline = False)

            except:
                pass

            return await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(Help(bot))
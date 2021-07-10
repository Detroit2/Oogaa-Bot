import discord
from discord.ext import commands
import keep_alive
import os
import json

client = commands.Bot(command_prefix="-", case_insensitive=True)
client.remove_command("help")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#start
@client.event
async def on_ready():
    print("The bot is ready to go!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="OOGAA BOOGA! Join our server! Code: nSyn75Ny7u"))

#on_message event
@client.event
async def on_message(message):
    x = message.content

    if x.lower() == "ooga booga" and message.author.id != 863038929199956019:
        await message.channel.send(f"OOGA BOOGA")

    with open("afk.json", "r") as f:
        afk = json.load(f)

    if message != None:
        if str(message.guild.id) in afk:
            if str(message.author.id) in afk[str(message.guild.id)]:
                del afk[str(message.guild.id)][str(message.author.id)]

                with open("afk.json", "w") as f:
                    json.dump(afk, f, indent=4)

                await message.channel.send(f"Welcome back {message.author.mention}! I have removed your afk message now!")

        else:
            try:
                for i in afk[str(message.guild.id)]:
                    test = await client.fetch_user(int(i))

                    if test in message.mentions:
                        m = afk[str(message.guild.id)][i]["message"]
                        em = discord.Embed(title=f"{test.name} is currently afk!\n\n{test.name}'s afk message: {m}", color=message.author.color)
                        image = afk[str(message.guild.id)][i]["image"]
                        
                        if image == "None":
                            await message.channel.send(embed=em)

                        else:
                            em.set_image(url=image)
                            await message.channel.send(embed=em)

            except:
                pass

    await client.process_commands(message)

#load command
@client.command()
async def load(ctx, extension):
    if ctx.author.id == 796042231538122762:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"Succesfully loaded {extension}!")
        return

    await ctx.send(f"You don't have permission to use that command!")

#unload command
@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 796042231538122762:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f"Succesfully unloaded {extension}!")
        return

    await ctx.send(f"You dont have permission to use that command!")

#reload command
@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 796042231538122762:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"Succesfully reloaded {extension}")
        return

    await ctx.send(f"You dont have permission to use that command!")

#ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')

#all errors

#load error
@load.error
async def load_error(ctx, error):
    await ctx.send(error)

#unload error
@unload.error
async def unload_error(ctx, error):
    await ctx.send(error)

#reload error
@reload.error
async def reload_error(ctx, error):
    await ctx.send(error)

#on_command_error error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command is invalid")
        return
        
    raise error

keep_alive.keep_alive()
#run event
token = os.environ.get("Token")
client.run(token)
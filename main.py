import discord
from discord.ext import commands
import keep_alive
import os
import json
import PIL

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

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

#get_mention_data function
async def get_mention_data():
    with open("mention.json", "r") as f:
        m = json.load(f)
    
    return m

#open_mention function
async def open_mention(user):
    users = await get_mention_data()

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = 0

    with open("mention.json", "w") as f:
        json.dump(users, f, indent=4)

    return True

#add_mention function
async def add_mention(user, amt):
    users = await get_mention_data()
    users[str(user.id)] += int(amt)

    with open("mention.json", "w") as f:
        json.dump(users, f, indent=4)

#remove_mention function
async def remove_mention(user):
    users = await get_mention_data()
    del users[str(user.id)]

    with open("mention.json", "w") as f:
        json.dump(users, f, indent=4)

#open_lvl function
async def open_lvl(user):
    users = await get_lvl_data()

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["level"] = 1
        users[str(user.id)]["experience"] = 0

    with open("level.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#get_lvl_data function
async def get_lvl_data():
    with open("level.json", "r") as f:
        users = json.load(f)

    return users

#add_experience function
async def add_experience(user, exp):
    users = await get_lvl_data()

    users[str(user.id)]["experience"] += exp

    with open("level.json", "w") as f:
        json.dump(users, f, indent=4)

#level_up function
async def level_up(user):
    users = await get_lvl_data()

    experience = users[str(user.id)]["experience"]
    lvl_start = users[str(user.id)]["level"]
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        channel = client.get_channel(863800186680901643)
        await channel.send(f"Congrats {user.mention}! You have leveled up to level {lvl_end}! Keep it up!")
        users[str(user.id)]["level"] = lvl_end
        with open("level.json", "w") as f:
            json.dump(users, f, indent=4)

#levelon_open function
async def levelon_open(server):
    users = await levelon_data()

    if str(server.id) in users:
        return False

    else:
        users[str(server.id)] = {}
        users[str(server.id)]["levelon"] = "off"

    with open("levelon.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#levelon_data function
async def levelon_data():
    with open("levelon.json", "r") as f:
        users = json.load(f)

    return users

#levelsettings
@client.command()
@commands.has_permissions(manage_channels=True)
async def levelsettings(ctx, mode = None):
    syntax = "```yml\nSyntax: .levelsettings (mode)\nExample Usage: .levelsettings on```"

    if mode == None:
        embed = discord.Embed(title=":negative_squared_cross_mark: Please specify the mode! The mode can only be `on`/`off`\n\n", description=syntax, color=discord.Color.red())
        await ctx.send(embed=embed)
        return     

    if mode.lower() != "on" and mode.lower() != "off":
        embed = discord.Embed(title=":negative_squared_cross_mark: The mode arguement can only be `on`/`off`\n\n", description=syntax, color=discord.Color.red())
        await ctx.send(embed=embed)
        return  

    await levelon_open(ctx.guild)
    users = await levelon_data()

    server = ctx.guild

    if users[str(server.id)]["levelon"] == "on" and mode.lower() == "on":
        embed = discord.Embed(title=":negative_squared_cross_mark: The levelling system is already on!\n\n", description=syntax, color=discord.Color.red())
        await ctx.send(embed=embed)
        return  

    if users[str(server.id)]["levelon"] == "off" and mode.lower() == "off":
        embed = discord.Embed(title=":negative_squared_cross_mark: The levelling system is already off!\n\n", description=syntax, color=discord.Color.red())
        await ctx.send(embed=embed)
        return  

    users[str(server.id)]["levelon"] = mode.lower()

    with open("levelon.json", "w") as f:
        json.dump(users, f, indent=4)

    await ctx.send(f"Successfully changed the levelsettings mode to `{mode.lower()}`")

#level command
@client.command()
async def level(ctx, member: discord.Member = None):
    await levelon_open(ctx.guild)
    users = await levelon_data()
    server = ctx.guild

    if users[str(server.id)]["levelon"] == "on":
        if member == None:
            member = ctx.author

        level = Image.open("level.png")

        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((128,127))

        level.paste(pfp, (105,34))

        await open_lvl(member)
        users = await get_lvl_data()

        draw = ImageDraw.Draw(level)
        font = ImageFont.truetype("level.ttf", 40)

        l = users[str(member.id)]["level"]
        e = users[str(member.id)]["experience"]

        draw.text((355, 75), f": {member.name}", (0, 0, 0), font=font)
        draw.text((232, 180), f": {l}", (0, 0, 0), font=font)
        draw.text((220, 242), f": {e}", (0, 0, 0), font=font)

        level.save("lev.png")

        await ctx.send(file=discord.File("lev.png"))

        return

    await ctx.send("The leveling system is currently off! Inorder to use it turn it on!")

#rank command
@client.command(aliases=["lb"])
async def leaderboard(ctx, x = 3):
    syntax = "```yml\nSyntax: .leaderboard (number)\nExample Usage: .leaderboard 3```"

    if x <= 0:
        embed = discord.Embed(title=":negative_squared_cross_mark: The number can't be less than or equal to 0\n\n", description=syntax, color=discord.Color.red())
        await ctx.send(embed=embed)
        return     

    await levelon_open(ctx.guild)
    users = await levelon_data()
    server = ctx.guild

    if users[str(server.id)]["levelon"] == "off":
        await ctx.send("The leveling system is currently off! Inorder to use it turn it on!")
        return

    users = await get_lvl_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["experience"] + 0
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(title=f"Top {x} experienced people", description="This is decided on the basis of the experience they have!", color=discord.Color.green())
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = await client.fetch_user(int(id_))
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)

#on_message event
@client.event
async def on_message(message):
    x = message.content

    if x.lower() == "ooga booga" and message.author.id != 863038929199956019:
        await message.channel.send(f"OOGA BOOGA")

    with open("afk.json", "r") as f:
        afk = json.load(f)            

    await levelon_open(message.guild)
    users = await levelon_data()
    server = message.guild

    if users[str(server.id)]["levelon"] == "on":
        if message.author.bot == True:
                return

        await open_lvl(message.author)
        await add_experience(message.author, 5)
        await level_up(message.author)

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
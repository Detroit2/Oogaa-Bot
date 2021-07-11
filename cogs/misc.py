import discord
from discord.ext import commands
import json
import asyncio
import pythonroblox
u = pythonroblox.User()

#get_afk_data function
async def get_afk_data():
    with open("afk.json", "r") as f:
        users = json.load(f)

    return users

#open_afk function
async def open_afk(server):
    users = await get_afk_data()

    if str(server) in users:
        return False

    else:
        users[str(server)] = {}

    with open("afk.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#add_afk function
async def add_afk(server, user, message, image):
    users = await get_afk_data()

    users[str(server)] = {}
    users[str(server)][str(user.id)] = {}
    users[str(server)][str(user.id)]["message"] = message
    users[str(server)][str(user.id)]["image"] = image

    with open("afk.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#get_snipe_data function
async def get_snipe_data():
    with open("snipe.json", "r") as f:
        users = json.load(f)

    return users

#open_snipe function
async def open_snipe(server):
    users = await get_snipe_data()

    if str(server) in users:
        return False

    else:
        users[str(server)] = {}

    with open("snipe.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#get_number_data function
async def get_number_data():
    with open("number.json", "r") as f:
        users = json.load(f)

    return users

#open_number function
async def open_number(server):
    users = await get_number_data()

    if str(server) in users:
        return False

    else:
        users[str(server)] = {}
        users[str(server)]["2"] = 1

    with open("number.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#add_number function
async def add_number(server):
    users = await get_number_data()

    n = users[str(server)]["2"]
    users[str(server)]["2"] =  n + 1

    with open("number.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#add_snipe function
async def add_snipe(server, message, time, author, channel):
    users = await get_snipe_data()
    number = await get_number_data()
    n = number[str(server)]["2"]
    s = 0
    for l in users[str(server)]:
        s += 1

    if s < 4:
        users[str(server)][str(n)] = {}
        users[str(server)][str(n)]["message"] = str(message)
        users[str(server)][str(n)]["time"] = str(time)
        users[str(server)][str(n)]["author"] = str(author)
        users[str(server)][str(n)]["channel"] = str(channel)

    else:
        sum = 0
        for i in users[str(server)]:
            if sum == 0:
                x = i
                del users[str(server)][x]
                users[str(server)][str(n)] = {}
                users[str(server)][str(n)]["message"] = str(message)
                users[str(server)][str(n)]["time"] = str(time)
                users[str(server)][str(n)]["author"] = str(author)
                users[str(server)][str(n)]["channel"] = str(channel)
                with open("snipe.json", "w") as f:
                    json.dump(users,f,indent=4)
                return

    with open("snipe.json", "w") as f:
        json.dump(users,f,indent=4)

    return True

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('misccmds file is ready')

    #message_delete
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await open_number(message.guild.id)
        await open_snipe(message.guild.id)
        await add_snipe(message.guild.id, message.content, message.created_at, message.author.id, message.channel.name)
        await add_number(message.guild.id)

    #snipe command
    @commands.command()
    async def snipe(self, ctx, number: int = None):
        if number == None:
            number = 1

        if number > 4:
            await ctx.send("The number artribute can be only smaller than or equal to 4!")
            return

        number -= 1
        await open_number(ctx.guild.id)
        await open_snipe(ctx.guild.id)
        users = await get_snipe_data()
        sum = 0
        for i in users[str(ctx.guild.id)]:
            if sum == number:
                message = users[str(ctx.guild.id)][i]["message"]
                time = users[str(ctx.guild.id)][i]["time"]
                channel = users[str(ctx.guild.id)][i]["channel"]
                id_ = users[str(ctx.guild.id)][i]["author"]
                author = await self.client.fetch_user(int(id_))
                em = discord.Embed(description=message, color=ctx.author.color)
                em.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
                em.set_footer(text=f"Deleted in : #{channel}")
                await ctx.send(embed=em)
                return
            
            sum += 1

    #roblox command
    @commands.command()
    async def roblox(self, ctx, username = None):
        if username == None:
            await ctx.send("Please provide the username next time!")
            return

        async with ctx.typing():
            result  = u.search_name(username)
            em = discord.Embed(title=f"{username}'s Roblox Profile")
            em.add_field(name="**Id:**", value=f"`{result.id}`")
            em.add_field(name="**Banned:**", value=f"`{result.banned}`")
            em.add_field(name="**Creation Date:**", value=f"`{result.created_date}`")
            em.add_field(name="**Display Name:**", value=f"`{result.displayName}`")
            em.add_field(name="**Friends Count:**", value=f"`{result.friends_count}`")
            em.add_field(name="**Followers Count:**", value=f"`{result.followers_count}`")
            em.add_field(name="**Following Count:**", value=f"`{result.following_count}`")
            em.add_field(name="**Groups Count:**", value=f"`{result.number_groups}`")
            em.add_field(name="**Description:**", value=f"`{result.description}`")
            em.add_field(name="**Status:**", value=f"`{result.status}`")
            em.set_thumbnail(url=str(result.avatar_url))
        
        await ctx.send(embed=em)

    #afk command
    @commands.command()
    async def afk(self, ctx, *, message = None):
        await open_afk(ctx.guild.id)

        if message == None:
            await ctx.send("Please provide a message to be sent when somone pings you while your afk next time!")
            return          

        await ctx.send("Do you want any gif to your afk embed? If yes then type `yes` otherwise type `no`")
        em = discord.Embed(title=f"Successfully done!\n\nAfk message: {message}", color=discord.Color.green())

        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 30,
                check = lambda message: message.author == ctx.author
                               and message.channel == ctx.channel
                )

            if msg:
                t = msg.content

                if t.lower() == "yes":
                    await ctx.send("Please send your image url!")

                    try:
                        msg = await self.client.wait_for(
                            "message",
                            timeout = 30,
                            check = lambda message: message.author == ctx.author
                                           and message.channel == ctx.channel
                            )

                        if msg:
                            em.set_image(url=msg.content)
                            await ctx.send(embed=em)
                            await add_afk(ctx.guild.id, ctx.author, message, msg.content)
                            return

                    except asyncio.TimeoutError:
                        await ctx.send(f'You were late to response')
                        return

                if t.lower() == "no":
                    await add_afk(ctx.guild.id, ctx.author, message, "None")
                    await ctx.send(embed=em)
                    return

                else:
                    await ctx.send("That's not a valid option!")
                    return

        except asyncio.TimeoutError:
            await ctx.send(f'You were late to response')
            return

    #all errors

    #roblox error
    @roblox.error
    async def roblox_error(self, ctx, error):
        await ctx.send(f"Coudn't find a user on roblox with that username!")

def setup(client):
    client.add_cog(Misc(client))
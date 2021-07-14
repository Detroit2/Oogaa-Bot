from discord.ext import commands

class Config(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('config file is ready')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.client.get_channel(862292095247187969)
        guild = await self.client.get_guild(862276149341192192)
        await channel.send(f"{member.mention} has joined the server! We have **{guild.member_count}** now!")

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        channel = await self.client.get_channel(862292095247187969)
        guild = await self.client.get_guild(862276149341192192)
        await channel.send(f"{member.mention} has left the server.. We have **{guild.member_count}** now.")

def setup(client):
    client.add_cog(Config(client))
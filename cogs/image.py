import discord
from discord.ext import commands
import random
import aiohttp

class Image(commands.Cog):

    def __init__(self, client):
        self.client = client

    #on_ready event
    @commands.Cog.listener()
    async def on_ready(self):
        print('imagecmds file is ready')

    #meme command
    @commands.command()
    async def meme(self, ctx):
      subreddit = ['memes','dankmeme']
      subredditt = random.choice(subreddit)

      async with aiohttp.ClientSession() as cs:
          async with cs.get(f"https://www.reddit.com/r/{subredditt}/new.json?sort=hot,") as data:
              res = await data.json()
              choose = res['data']['children'] [random.randint(0, 25)]
              title = choose['data']['title']
              standard = 'https://www.reddit.com'
              lin = choose['data']['permalink']
              newlink = standard + lin
              embed = discord.Embed(description= f'[{title}]({newlink})')
              embed.set_image(url= choose['data']['url'] )
              likes = choose['data']['ups']
              replies = choose['data']['num_comments']
              embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
              await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Image(client))
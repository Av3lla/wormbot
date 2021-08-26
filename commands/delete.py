import discord
from discord.ext import commands


class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["clear", "delete"])
    async def 지우기(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'{ctx.author} 님이 "{amount}" 만큼의 메세지를 삭제합니다.')


def setup(bot):
    bot.add_cog(Delete(bot))
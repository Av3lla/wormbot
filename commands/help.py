import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 도움말(self, ctx):
        wormhelp = embed=discord.Embed(title="도움말", description="Help", color=0xff5733)
        embed.add_field(name="/도움말", value="도움말을 표시합니다.", inline=False)
        embed.add_field(name="/지우기 (개수)", value="설정한 만큼 최근 대화기록을 삭제합니다.", inline=False)
        embed.add_field(name="/따라하기", value="내가 한 말을 따라합니다.", inline=False)
        embed.set_footer(text="Made by @Avella#8448")
        await ctx.send(embed=wormhelp)


def setup(bot):
    bot.add_cog(Help(bot))
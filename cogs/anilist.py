import discord
import kadal
from discord.ext import commands
from kadal import MediaNotFound

MAL_ICON = 'https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png'
AL_ICON = 'https://avatars2.githubusercontent.com/u/18018524?s=280&v=4'


class Anilist:
    def __init__(self, bot):
        self.bot = bot
        self.klient = kadal.Client()
        self.t_client = bot.t_client

    @commands.command(name="manga")
    async def al_manga(self, ctx, *, query):
        """Searches Anilist for a Manga."""
        async with ctx.typing():
            try:
                result = await self.klient.search_manga(query, popularity=True)
            except MediaNotFound:
                return await ctx.send(":exclamation: Manga was not found!")
            except Exception as e:
                return await ctx.send(f":exclamation: An unknown error occurred:\n{e}")
        if len(result.description) > 1024:
            result.description = result.description[:1024 - (len(result.site_url) + 7)] + f"[...]({result.site_url})"
        em = discord.Embed(title=result.title['english'] or result.title['romaji'], colour=0xFF9933)
        em.description = ", ".join(result.genres)
        em.url = result.site_url
        em.add_field(name="Japanese Title", value=result.title['native'], inline=True)
        em.add_field(name="Type", value=str(result.format.name).replace("_", " ").capitalize(), inline=True)
        em.add_field(name="Chapters", value=result.chapters or "?", inline=True)
        em.add_field(name="Volumes", value=result.volumes or "?", inline=True)
        em.add_field(name="Score", value=str(result.average_score / 10) + " / 10" if result.average_score else "?",
                     inline=False)
        em.add_field(name="Status", value=str(result.status.name).replace("_", " ").capitalize(), inline=True)
        (year, month, day) = result.start_date.values()
        published = f"{day}/{month}/{year}"
        (year, month, day) = result.end_date.values() if result.end_date['day'] else ('?', '?', '?')
        published += f" - {day}/{month}/{year}"
        em.add_field(name="Published", value=published, inline=True)
        em.add_field(name="Synopsis", value=result.description, inline=False)
        em.add_field(name="Link", value=result.site_url, inline=False)
        em.set_author(name='Anilist', icon_url=AL_ICON)
        em.set_thumbnail(url=result.cover_image)
        await ctx.send(embed=em)

    @commands.command(name="anime")
    async def al_anime(self, ctx, *, query):
        """Searches Anilist for an Anime."""
        async with ctx.typing():
            try:
                result = await self.klient.search_anime(query, popularity=True)
            except MediaNotFound:
                return await ctx.send(":exclamation: Anime was not found!")
            except Exception as e:
                return await ctx.send(f":exclamation: An unknown error occurred:\n{e}")
        if len(result.description) > 1024:
            result.description = result.description[:1024 - (len(result.site_url) + 7)] + f"[...]({result.site_url})"
        em = discord.Embed(title=result.title['english'] or result.title['romaji'], colour=0x02a9ff)
        em.description = ", ".join(result.genres)
        em.url = result.site_url
        em.add_field(name="Japanese Title", value=result.title['native'], inline=True)
        em.add_field(name="Type", value=str(result.format.name).replace("_", " ").capitalize(), inline=True)
        em.add_field(name="Episodes", value=result.episodes or "?", inline=True)
        em.add_field(name="Score", value=str(result.average_score / 10) + " / 10" if result.average_score else "?",
                     inline=False)
        em.add_field(name="Status", value=str(result.status.name).replace("_", " ").capitalize(), inline=True)
        (year, month, day) = result.start_date.values()
        aired = f"{day}/{month}/{year}"
        (year, month, day) = result.end_date.values() if result.end_date['day'] else ('?', '?', '?')
        aired += f" - {day}/{month}/{year}"
        em.add_field(name="Aired", value=aired, inline=True)
        em.add_field(name="Synopsis", value=result.description, inline=False)
        em.add_field(name="Link", value=result.site_url, inline=False)
        em.set_author(name='Anilist', icon_url=AL_ICON)
        em.set_thumbnail(url=result.cover_image)
        await ctx.send(embed=em)

    @commands.command(name="user")
    async def al_user(self, ctx, *, query):
        """Searches Anilist for a User"""
        async with ctx.typing():
            try:
                result = await self.klient.search_user(query)
            except MediaNotFound:
                return await ctx.send(":exclamation: User was not found!")
            except Exception as e:
                return await ctx.send(f":exclamation: An unknown error occurred:\n{e}")
        if result.about and len(result.about) > 2000:
            result.about = result.about[:2000 - (len(result.site_url) + 7)] + f"[...]({result.site_url})"
        em = discord.Embed(title=result.name, color=0x02a9ff)
        em.description = result.about
        em.url = result.site_url
        em.add_field(name="Days Watched", value=round(result.stats.watched_time / 60 / 24, 2))
        em.add_field(name="Chapters Read", value=result.stats.chapters_read)
        em.set_author(name='Anilist', icon_url=AL_ICON)
        em.set_thumbnail(url=result.avatar)
        if result.banner_image:
            em.set_image(url=result.banner_image)
        await ctx.send(embed=em)

    @commands.command(name="next")
    async def al_next(self, ctx, *, query):
        """Countdown for the next episode of an airing Anime"""
        async with ctx.typing():
            try:
                result = await self.klient.search_anime(query)
            except MediaNotFound:
                return await ctx.send(":exclamation: Anime was not found!")
            except Exception as e:
                return await ctx.send(f":exclamation: An unknown error occurred:\n{e}")
        remaining = ''
        desc = None
        if result.status == kadal.MediaStatus.RELEASING:
            minutes, seconds = divmod(result.airing.time_until.total_seconds(), 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            remaining = f"{int(days)} Days, {int(hours)} Hours, and {int(minutes)} Minutes"
            desc = f'Next episode: #{result.airing.episode}'
        elif result.status == kadal.MediaStatus.NOT_YET_RELEASED:
            remaining = "Anime hasn't started airing yet!"
        elif result.status == kadal.MediaStatus.FINISHED:
            remaining = "Anime has finished airing!:\n\n"
            (year, month, day) = result.end_date.values()
            remaining += f'{year}/{month}/{day}'
        embed = discord.Embed(title=next(filter(None, result.title.values())), color=0x02a9ff)
        embed.description = desc
        embed.url = result.site_url
        embed.add_field(name="Airs in", value=remaining)
        embed.set_footer(text='Anilist')
        embed.set_author(name='Anilist', icon_url=AL_ICON)
        embed.set_thumbnail(url=result.cover_image)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Anilist(bot))

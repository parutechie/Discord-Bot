import asyncio
import nextcord
from easy_pil import Editor, load_image_async, Font
from nextcord.ext import commands
from pytube import YouTube

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Play
    @nextcord.slash_command(description="Play a song")
    async def play(self, ctx, url: str):
        try:
            voice_channel = ctx.user.voice.channel
            voice_state = ctx.user.voice
            voice_client = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)

            if not voice_client:
                try:
                    voice_client = await voice_channel.connect()
                except Exception as e:
                    await ctx.send("Could not connect to the voice channel. Please check bot permissions.")
                    print(e)
                    return
            elif voice_state.channel != voice_client.channel:
                try:
                    await voice_client.move_to(voice_channel)
                except Exception as e:
                    await ctx.send("Could not move to the desired voice channel. Please check bot permissions.")
                    print(e)
                    return

            try:
                yt = YouTube(url)
                video_url = yt.streams.filter(only_audio=True).first().url

                voice_client.stop()
                voice_client.play(nextcord.FFmpegPCMAudio(video_url))

                embed = nextcord.Embed(
                    title="Now Playing",
                    description=f"**[{yt.title}]({url})** Duration: **{yt.length}**",
                    color=nextcord.Color.dark_purple()
                )
                embed.set_thumbnail(url=yt.thumbnail_url)
                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send("An error occurred while trying to play the song.")
                print(e)

        except AttributeError:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

    #pause
    @nextcord.slash_command(description="Pause the playback")
    async def pause(self, ctx):
        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_playing():
            voice_client.pause()
            embed = nextcord.Embed(
                title='Playback paused....',
                color=nextcord.Color.dark_purple()
                
            )
            message = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await message.delete()
        else:
            embed = nextcord.Embed(
                title='No Playback to pause....',
                color=nextcord.Color.dark_purple()
            )
            message = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await message.delete()
            

    #resume
    @nextcord.slash_command(description="Resume the playback")
    async def resume(self, ctx):
        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_paused():
            voice_client.resume()
            embed = nextcord.Embed(
                title='Playback resumed....',
                color=nextcord.Color.dark_purple()
            )
            message = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await message.delete()
        else:
            embed = nextcord.Embed(
                title='No playback to resume....',
                color=nextcord.Color.dark_purple()
            )
            message = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await message.delete()

    #stop
    @nextcord.slash_command(description="Stop the playback")
    async def stop(self, ctx):
        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
            voice_client.stop()
            await voice_client.disconnect()
            embed = nextcord.Embed(
                title='Stopped the playback...',
                color=nextcord.Color.dark_purple()
            )
            message = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await message.delete()
        else:
            embed = nextcord.Embed(
                title='No playback is currently available',
                color=nextcord.Color.dark_purple()
            )
            message = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await message.delete()

    #leave
    @nextcord.slash_command(description="Leave the voice channel")
    async def leave(self, interaction):
        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        
        if voice_client:
            await voice_client.disconnect()
            embed = nextcord.Embed(
                title='Left the voice channel...',
                color=nextcord.Color.dark_purple()
            )
            message = await interaction.response.send_message(embed=embed)
            await asyncio.sleep(20)
            await message.delete()
        else:
            embed = nextcord.Embed(
                title='Not connected to a voice channel...',
                color=nextcord.Color.dark_purple()
            )
            message = await interaction.response.send_message(embed=embed)
            await asyncio.sleep(20)
            await message.delete()

def setup(bot):
    bot.add_cog(MusicCog(bot))

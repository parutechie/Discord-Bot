import nextcord
from nextcord.ext import commands
from easy_pil import Editor, load_image_async, Font

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = "YOUR_CHANNEL_ID"  
        self.poppins = Font.poppins(size=50, variant="bold")
        self.poppins_small = Font.poppins(size=20, variant="light")

    def ordinal(self, n):
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            return

        background = Editor('welcome_image.jpg')
        profile_image = await load_image_async(str(member.display_avatar.url))
        profile = Editor(profile_image).resize((335, 335)).circle_image()  #IMAGE SIZE

        background.paste(profile, (99, 90))
        background.ellipse((99, 90), 335, 335, outline='white', stroke_width=7) #STROKE SIZE

        welcome_text = f'Welcome to {member.guild.name}!'
        member_count = self.ordinal(sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None))

        file = nextcord.File(fp=background.image_bytes, filename='welcome_image.jpg')
        await channel.send(f'hey {member.mention} {welcome_text} ;)')
        await channel.send(file=file)
        await channel.send(f'You are the {member_count} member of {member.guild.name} Community')

def setup(bot):
    bot.add_cog(WelcomeCog(bot))

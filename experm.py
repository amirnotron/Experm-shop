import discord
import asyncio
import os
from datetime import timezone, timedelta , datetime
from discord.ext import commands , tasks
from discord import app_commands
from discord import ui, Embed , File

IRAN_TIMEZONE = timezone(timedelta(hours=3, minutes=30))

token = ""

intents = discord.Intents.all()

is_watching = True

MINECRAFT_PIC_PATH = './Image/minecraft-pic.jpg'

MIGRATE_PIC_PATH = './Image/Migrate.jpg'

TICKET_CHANNEL_URL = "https://discord.com/channels/1204858888235646986/1373786825382035497"

bot = commands.Bot(command_prefix="!", intents=intents)

class McMyView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        pass

    @discord.ui.button(label="اکانت ماینکرفت", style=discord.ButtonStyle.red, custom_id="mc_account_initial")
    async def mc_account_initial_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        minecraft_image_file = None
        try:
            minecraft_image_file = File(MINECRAFT_PIC_PATH, filename="ephemeral_minecraft_image.jpg")
        except FileNotFoundError:
            await interaction.followup.send("Error: Minecraft image file not found! Please check the path and filename.", ephemeral=True)
            return

        mc_embed = Embed(
            title="**اکانت ماینکرفت**",
            description="""
**
[ Minecraft Account ]

اکانت ماینکرفت فول اکسس ( FA ) مایکروسافت دارای قابلیت عوض کردن اسکین . یوزرنیم . ایمیل . پسورد ....  و کازمتیک هستن --------------------- اکانت فول اکسس FA | قیمت 799 هزار تومان 

اکانت آنلاکد فول اکسس پرمیوم ( UFA ) مایکروسافت اکانت های فول اکسس آنلاکد ماینکرفت مستقیم رو ایمیل یا اکانت خودتون خریداری میشه و همه قابلیت های اکانت فول اکسس مایکروسافت ( FA ) رو داره ------------------------------- اکانت فول اکسس UFA | قیمت  1,799 هزار تومان 

**
            """,
            color=discord.Color.dark_red(),
            timestamp=datetime.now(IRAN_TIMEZONE)
        )
        mc_embed.set_image(url=f"attachment://{minecraft_image_file.filename}")

        view_for_mc_response = ui.View(timeout=None)

        ticket_button_mc = discord.ui.Button(
            label="Ticket",
            style=discord.ButtonStyle.url,
            url="https://discord.com/channels/1204858888235646986/1373786825382035497"
        )
        view_for_mc_response.add_item(ticket_button_mc)

        await interaction.followup.send(
            embed=mc_embed,
            view=view_for_mc_response,
            ephemeral=True,
            file=minecraft_image_file
        )

    @discord.ui.button(label="کیپ های ماینکرفت", style=discord.ButtonStyle.red, custom_id="mc_capes_initial")
    async def mc_cape_initial_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        mc_cape_embed = Embed(
            title="**فروش تمامی کیپ های ماینکرافت کاملا قانونی**",
            description="""
**
👇 👇 👇 برای اطلاع از قیمت روی کیپ مورد نظرتون کلیک کنید
**
            """,
            color=discord.Color.dark_red(),
            timestamp=datetime.now(IRAN_TIMEZONE)
        )

        cape_pricing_view = ui.View(timeout=None)
        migrate_button = discord.ui.Button(label="Migrate", style=discord.ButtonStyle.red, custom_id="migrate_cape_button_dynamic")
        
        migrate_button.callback = self._handle_migrate_button_click 
        
        cape_pricing_view.add_item(migrate_button)

        await interaction.followup.send(
            embed=mc_cape_embed,
            ephemeral=True,
            view=cape_pricing_view
        )

    async def _handle_migrate_button_click(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        migrate_image_file = None
        try:
            migrate_image_file = File(MIGRATE_PIC_PATH, filename="ephemeral_migrate_image.jpg")
        except FileNotFoundError:
            await interaction.followup.send("Error: Minecraft image file not found! Please check the path and filename.", ephemeral=True)
            return

        migration_details_embed = Embed(
            title="**کیپ میگریت**",
            description="""
**
👇👇👇 کیپ میگراتور  ....... | قیمت | 899 
**
            """,
            color=discord.Color.dark_red(),
            timestamp=datetime.now(IRAN_TIMEZONE)
        )

        migration_details_embed.set_image(url=f"attachment://{migrate_image_file.filename}")

        ticket_link_view = ui.View(timeout=None)
        go_to_ticket_button = discord.ui.Button(label="Ticket", style=discord.ButtonStyle.url, url=TICKET_CHANNEL_URL)
        ticket_link_view.add_item(go_to_ticket_button)

        await interaction.followup.send(
            embed=migration_details_embed,
            ephemeral=True,
            view=ticket_link_view,
            file=migrate_image_file
        )

@tasks.loop(seconds=15)
async def change_status():
    global is_watching
    for guild in bot.guilds:
        if is_watching:
            await bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guild.member_count} Members"))
        else:
            await bot.change_presence(status=discord.Status.dnd,activity=discord.Streaming(url='https://www.twitch.tv/thedaniyal_official',name='X-PERM | SHOP'))
    is_watching = not is_watching

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    elif message.content.lower() == "time":
        await message.channel.send(f"The current time in Iran is: {IRAN_TIMEZONE}")
    elif message.content.lower() == "mcbutton":
        embed = Embed(title="خدمات ماینکرفت", description="تمامی خدمات ماینکرفت انجام میشود", color=discord.Color.dark_red())
        view = McMyView()
        await message.channel.send(embed=embed, view=view)

    await bot.process_commands(message)

@bot.event
async def on_ready():
    try:
        await bot.load_extension('commands')
        print("Extension 'commands' loaded.")
    except Exception as e:
        print(f"Failed to load extension 'commands': {e}")
    change_status.start()
    bot.add_view(McMyView())
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)

async def main_bot():
    print("Bot is starting...")
    await bot.start(token,reconnect=True)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(main_bot()))

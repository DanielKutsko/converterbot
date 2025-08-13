import os
import re
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = "https://v6.exchangerate-api.com/v6/d9f4dc18231059d9491e5533/latest/"

# Настройка бота
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Регулярка для поиска суммы и валюты
pattern = r"(\d+(?:\.\d+)?)\s*(USD|EUR|PLN|GBP|UAH)"

@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    match = re.search(pattern, message.content, re.IGNORECASE)
    if match:
        amount = float(match.group(1))
        currency = match.group(2).upper()

        response = requests.get(API_URL + currency)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("conversion_rates", {})

            if rates:
                eur = amount * rates.get("EUR", 0)
                pln = amount * rates.get("PLN", 0)
                uah = amount * rates.get("UAH", 0)
                gbp = amount * rates.get("GBP", 0)

                await message.channel.send(
                    f"💱 {amount} {currency}:\n"
                    f"🇪🇺 {eur:.2f} EUR\n"
                    f"🇵🇱 {pln:.2f} PLN\n"
                    f"🇺🇦 {uah:.2f} UAH\n"
                    f"🇬🇧 {gbp:.2f} GBP"
                )

    await bot.process_commands(message)

bot.run(TOKEN)

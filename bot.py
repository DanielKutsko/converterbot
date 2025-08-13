import re
import requests
import discord
from discord.ext import commands

API_KEY = ""  # Вставь сюда свой API ключ
TOKEN = ""    # Вставь сюда свой Discord токен

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CURRENCY_KEYWORDS = {
    "usd": "USD", "dolar": "USD", "dolary": "USD", "dolarów": "USD", "$": "USD",
    "eur": "EUR", "euro": "EUR", "€": "EUR",
    "pln": "PLN", "zloty": "PLN", "zł": "PLN",
    "uah": "UAH", "hrywna": "UAH", "hryw": "UAH",
    "gbp": "GBP", "funt": "GBP", "£": "GBP"
}

def convert_currency(amount, from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
    r = requests.get(url).json()
    if r.get("result") == "error":
        return None
    return r.get("conversion_result")

@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content.lower()
    matches = re.findall(r"(\d+(?:[.,]\d+)?)\s*([a-zA-Ząćęłńóśźż$€£]+)", text)

    if matches:
        reply_lines = []
        for amount_str, currency_word in matches:
            try:
                amount = float(amount_str.replace(",", "."))
            except ValueError:
                continue

            from_currency = None
            for word, code in CURRENCY_KEYWORDS.items():
                if word in currency_word:
                    from_currency = code
                    break

            if from_currency:
                target_currencies = ["USD", "EUR", "UAH", "PLN", "GBP"]
                target_currencies.remove(from_currency)
                results = []
                for cur in target_currencies:
                    converted = convert_currency(amount, from_currency, cur)
                    if converted is not None:
                        results.append(f"{converted:.2f} {cur}")
                if results:
                    reply_lines.append(f"{amount} {from_currency} = " + ", ".join(results))

        if reply_lines:
            await message.channel.send("\n".join(reply_lines))

    await bot.process_commands(message)

bot.run(TOKEN)
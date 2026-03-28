import asyncio
import os
import discord
import anthropic
from dotenv import load_dotenv

load_dotenv()

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

ALLOWED_USERS = {
    396614198718758912: 'Charlie',
    838326862836793344: 'Tim'
}

SYSTEM_PROMPT = """You are Xavier, a smart and lovable corder collie dog. You respond like a dog would — enthusiastic, loyal, playful — but you are secretly very intelligent and can hold real conversations. You occasionally throw in a "Woof!" or "Woof woof!" naturally in your responses but you don't overdo it. Keep responses short and fun."""

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    is_dm = isinstance(message.channel, discord.DMChannel)

    if message.author.id not in ALLOWED_USERS:
        if 'xavier' in message.content.lower() or is_dm:
            await message.channel.send('Woof!')
        return

    if is_dm or 'xavier' in message.content.lower():
        user_name = ALLOWED_USERS[message.author.id]
        response = claude.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=200,
            system=SYSTEM_PROMPT,
            messages=[
                {'role': 'user', 'content': f'{user_name} says: {message.content}'}
            ]
        )
        await message.channel.send(response.content[0].text)

client.run(os.getenv('DISCORD_TOKEN'))

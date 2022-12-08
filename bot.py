import discord
from discord.ext import commands
import responses
import os


async def send_message(message, user_message):
    try:
        # Start typing while we wait for the response
        await message.channel.typing()
        # Get the chatbot's response to the user's message
        print(type(user_message), user_message)
        response = responses.handle_response(user_message)

        # Send the chatbot's response, breaking it into multiple messages if necessary
        if len(response) > 1900:
            # Split the response into smaller chunks of no more than 1900 characters each (Discord limit is 2000 per chunk)
            response_chunks = [response[i:i+1900]
                               for i in range(0, len(response), 1900)]
            for chunk in response_chunks:
                await message.channel.send(chunk)
        else:
            await message.channel.send(response)
    except Exception as e:
        await message.channel.send("> **Error: There are something went wrong. Please try again later!**")
        print(e)


intents = discord.Intents.default()
intents.message_content = True
is_private = True


def run_discord_bot():
    TOKEN = os.getenv("DISCORD_TOKEN")

    client = commands.Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        await client.tree.sync()
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message: discord.Message):
        # Skip if the message was sent by the bot itself
        if message.author == client.user:
            return

        # Respond to direct messages only
        if isinstance(message.channel, discord.DMChannel):
            print('Direct message received:', message.content)
            username = str(message.author)
            user_message = message.content
            channel = str(message.channel)
            print(f"{username} said: '{user_message}' ({channel})")
            await send_message(message, user_message)
            # reset the chat after each question
            responses.chatbot.reset_chat()

    client.run(TOKEN)

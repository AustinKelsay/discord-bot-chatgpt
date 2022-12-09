import discord
from discord.ext import commands
import responses
import os
import asyncio


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

    async def reset_chat_async(message):
        # Reset the chat
        responses.chatbot.reset_chat()

        # Send an interaction to the user
        interaction = discord.Interaction(
            type='message',
            text='The chat has been reset. Sadly I must reset every 5 minutes or discord will time me out'
        )
        await message.author.send(interaction)

        # Schedule the next call to reset_chat_async after 5 minutes
        asyncio.get_event_loop().call_later(300, reset_chat_async)

    @client.event
    async def on_ready():
        await client.tree.sync()
        print(f'{client.user} is now running!')

        # Start the first call to reset_chat_async
        asyncio.get_event_loop().create_task(reset_chat_async())

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

    client.run(TOKEN)

import discord
from discord import app_commands
from discord.ext import commands
import responses
import os


async def send_message(message, user_message):
    try:
        response = '> **' + user_message + '** - <@' + \
            str(message.user.id) + '>\n\n' + \
            responses.handle_response(user_message)
        if len(response) > 1900:
            # Split the response into smaller chunks of no more than 1900 characters each(Discord limit is 2000 per chunk)
            response_chunks = [response[i:i+1900]
                               for i in range(0, len(response), 1900)]
            for chunk in response_chunks:
                await message.followup.send(chunk)
        else:
            await message.followup.send(response)
    except Exception as e:
        await message.followup.send("> **Error: There are something went wrong. Please try again later!**")
        print(e)

intents = discord.Intents.default()
intents.message_content = True
is_private = True


def run_discord_bot():
    TOKEN = os.getenv("DISCORD_TOKEN")

    # Set the number of consecutive questions before resetting
    RESET_THRESHOLD = 5

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
            # Store the number of consecutive questions in a variable
            consecutive_questions = 0

            print('Direct message received:', message.content)
            username = str(message.author)
            user_message = message.content
            channel = str(message.channel)
            print(f"{username} said: '{user_message}' ({channel})")
            await send_message(message, user_message)

            # Increment the number of consecutive questions
            consecutive_questions += 1

            # Check if the threshold has been reached
            if consecutive_questions >= RESET_THRESHOLD:
                # Reset the conversation history and reset the counter
                responses.chatbot.reset_chat()
                consecutive_questions = 0

                # Send a followup message
                await message.channel.send("> **Info: I have forgotten everything.**")
                print("The CHAT BOT has been successfully reset")

    client.run(TOKEN)

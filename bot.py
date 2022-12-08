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

    # Store the number of consecutive questions in a variable
    consecutive_questions = 0

    @client.event
    async def on_ready():
        await client.tree.sync()
        print(f'{client.user} is now running!')

    @client.tree.command(name="chat", description="Have a chat with chatGPT")
    async def chat(interaction: discord.Interaction, *, message: str):
        global consecutive_questions

        print('Chat command received', message)
        if interaction.user == client.user:
            return
        username = str(interaction.user)
        user_message = message
        channel = str(interaction.channel)
        print(f"{username} said: '{user_message}' ({channel})")
        await interaction.response.defer(ephemeral=is_private)
        await send_message(interaction, user_message)

        # Increment the number of consecutive questions
        consecutive_questions += 1

        # Check if the threshold has been reached
        if consecutive_questions >= RESET_THRESHOLD:
            # Reset the conversation history and reset the counter
            responses.chatbot.reset_chat()
            consecutive_questions = 0

            # Send a followup message
            await interaction.followup.send("> **Info: I have forgotten everything.**")
            print("The CHAT BOT has been successfully reset")

    client.run(TOKEN)

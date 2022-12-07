import discord
import responses
import os

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)


def run_discord_bot():
    # Change your token here
    global client
    if client == None:
        client = discord.Client(intents=intents)

    TOKEN = os.getenv("DISCORD_TOKEN")

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def send_message(message, user_message, is_private):
        # Get the response for the user's message
        response = responses.handle_response(user_message)

        try:
            # Send the response to the user
            await message.author.send(response)
        except Exception as e:
            # Print any errors that occur
            print("my exception", e)
            await message.channel.send("Sorry I timed out trying to send you a message. Please try again.")

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)

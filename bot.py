import discord
import responses
import os
import asyncio


SEND_MESSAGE_DELAY = 1


async def send_message(message, user_message, is_private):
    try:
        # Get the response for the user's message
        response = responses.handle_response(user_message)

        # Split the response into smaller chunks if necessary
        if len(response) > 2000:
            response_chunks = [response[i:i+2000]
                               for i in range(0, len(response), 2000)]
        else:
            response_chunks = [response]

        # Send each chunk of the response, separated by a delay
        for chunk in response_chunks:
            if is_private:
                await message.author.send(chunk)
            else:
                await message.channel.send(chunk)

            # Wait before sending the next chunk
            await asyncio.sleep(SEND_MESSAGE_DELAY)

    except Exception as e:
        # Print any errors that occur
        print("my exception", e)

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
    async def on_message(message):
        if message.author == client.user:
            return

        # Check if the message was sent in a DM
        if message.channel.type == discord.ChannelType.private:
            username = str(message.author)
            user_message = str(message.content)

            with open("questions.txt", "a") as f:
                f.write(user_message + "\n")

            if user_message[0] == '?':
                user_message = user_message[1:]
                await send_message(message, user_message, is_private=True)
            else:
                await send_message(message, user_message, is_private=False)

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)

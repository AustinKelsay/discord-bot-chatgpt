import discord
import responses
import os
import time
import typing
import functools


def blocking_func(a, b, c=1):
    """A very blocking function"""
    time.sleep(a + b + c)
    return "some stuff"


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(
        blocking_func, *args, **kwargs)  # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await client.loop.run_in_executor(None, func)


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        # Run a blocking function in a non-blocking way before sending the response
        await run_blocking(blocking_func, 1, 2, c=3)
        if len(response) > 2000:
            # Split the response into smaller chunks of no more than 2000 characters each
            response_chunks = [response[i:i+2000]
                               for i in range(0, len(response), 2000)]
            for chunk in response_chunks:
                # Send each chunk separately
                await message.author.send(chunk) if is_private else await message.channel.send(chunk)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
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

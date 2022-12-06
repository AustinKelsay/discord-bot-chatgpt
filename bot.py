import discord
import responses
import os
import dotenv

dotenv.load_dotenv()

# Send messages
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
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


def run_discord_bot():
    # Change your token here
    TOKEN = os.getenv("DISCORD_TOKEN")
    client = discord.Client(intents=intents)

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

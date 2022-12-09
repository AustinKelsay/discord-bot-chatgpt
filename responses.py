from asyncChatGPT.asyncChatGPT import Chatbot
import os

config = {
    "email": os.getenv("EMAIL"),
    "password": os.getenv("PASSWORD"),
}

if os.getenv("SESSION"):
    config.update(session_token=os.getenv("SESSION"))

chatbot = Chatbot(config, conversation_id=None)


async def handle_response(prompt) -> str:
    chatbot.refresh_session()
    response = await chatbot.get_chat_response(prompt, output="text")
    responseMessage = response['message']

    return responseMessage

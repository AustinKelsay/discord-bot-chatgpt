from revChatGPT.revChatGPT import Chatbot
import os
import dotenv

dotenv.load_dotenv()

config = {
    "email": os.getenv("EMAIL"),
    "password": os.getenv("PASSWORD"),
}

if os.getenv("SESSION"):
    config.update(session_token=os.getenv("SESSION"))

chatbot = Chatbot(config, conversation_id=None)
chatbot.refresh_session()


def handle_response(prompt) -> str:
    response = chatbot.get_chat_response(prompt, output="text")
    responseMessage = response["message"]

    return responseMessage
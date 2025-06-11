import os
import json
from dotenv import load_dotenv
import chainlit as cl
from litellm import completion

# ✅ Load environment variables
load_dotenv(dotenv_path="E:/PyProjects/TransAgent/config.env")

# ✅ Get API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
print("Working Directory:", os.getcwd())
print("API Key:", gemini_api_key)

if not gemini_api_key:
    raise ValueError("API key is missing or not loaded from .env")

# ✅ Chat Start
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat history", [])
    await cl.Message(content="**Welcome to my Translator Agent**").send()

# ✅ Chat Message Handling
@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="Translating...")
    await msg.send()

    history = cl.user_session.get("chat history") or []
    history.append({"role": "user", "content": message.content})

    try:
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key=gemini_api_key,
            messages=history
        )
        response_content = response.choices[0].message.content

        msg.content = response_content
        await msg.update()

        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat history", history)
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()

# ✅ Chat End
@cl.on_chat_end
async def on_chat_end():
    history = cl.user_session.get("chat history") or []

    with open("translation_chat_history.json", "w") as f:
        json.dump(history, f, indent=2)

    print("Chat history saved")

from urllib import response
import chainlit as cl
from goldbot_agent import GoldBotAgent


agent = GoldBotAgent().agent()
cl.HaystackAgentCallbackHandler(agent)

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    response = await cl.make_async(agent.run)(message)
    answer = response["answers"][0].answer
    # Send a response back to the user
    await cl.Message(author="GoldBot", content=answer).send()
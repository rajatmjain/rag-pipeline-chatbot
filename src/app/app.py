from urllib import response
import chainlit as cl
from goldbot_agent import GoldBotAgent


agent = GoldBotAgent().agent()
cl.HaystackAgentCallbackHandler(agent)

@cl.on_message
async def main(message: str):
    # Your custom logic goes here...
    ans = await answer(query=message)
    # Send a response back to the user
    await cl.Message(author="GoldBot", content=ans).send()

async def answer(query:str) -> str:
    response = await agent.run(query=query)
    ans = response["answers"][0].answer

    return ans

# print(agent.run(query="What was the price of gold on October 5, 2023?"))


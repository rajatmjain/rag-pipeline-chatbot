import chainlit as cl
from goldbot_agent import GoldBotAgent


agent = GoldBotAgent().agent()
cl.HaystackAgentCallbackHandler(agent)

@cl.on_message
async def main(message: str):
    # Your custom logic goes here...
    response = await getAnswer(query=message)
    answer = response["answers"][0].answer
    # Send a response back to the user
    await cl.Message(author="GoldBot", content=answer).send()

async def getAnswer(query:str):
    answer = agent.run(query=query)
    return answer


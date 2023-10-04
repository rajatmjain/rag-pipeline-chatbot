import os
import chainlit as cl
from haystack.agents.conversational import ConversationalAgent
from haystack.nodes import PromptNode
from haystack.agents.memory import ConversationSummaryMemory


modelAPIKey = os.getenv("MODEL_API_KEY",None)
modelName = os.getenv("MODEL_NAME",None)


# Prompt Node
conversationalAgentPromptNode = PromptNode(modelName,api_key=modelAPIKey,max_length=256)

# Memory layer on top of Prompt Node
summaryMemory = ConversationSummaryMemory(conversationalAgentPromptNode)

agent = ConversationalAgent(
  prompt_node=conversationalAgentPromptNode,
  memory=summaryMemory,
)

cl.HaystackAgentCallbackHandler(agent)

@cl.on_message
async def main(message: str):
    # Your custom logic goes here...
    response = await cl.make_async(agent.run)(message)
    await cl.Message(author="Agent", content=response["answers"][0].answer).send()

    # Send a response back to the user
    # await cl.Message(
    #     content=f"Received: {message}",
    # ).send()

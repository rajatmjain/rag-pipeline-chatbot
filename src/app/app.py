import chainlit as cl
from haystack.agents.conversational import ConversationalAgent
from haystack.nodes import PromptNode
from haystack.agents.memory import ConversationSummaryMemory
import os

hfAPIKey = os.getenv("HF_API_KEY")
hfModelName = os.getenv("HF_MODEL_NAME")

promptNode = PromptNode(hfModelName,api_key=hfAPIKey,max_length=256)

summaryMemory = ConversationSummaryMemory(promptNode)

agent = ConversationalAgent(
    prompt_node=promptNode,
    memory=summaryMemory
    )

cl.HaystackAgentCallbackHandler(agent=agent)

@cl.on_message
async def main(message: str):
    # Your custom logic goes here...
    response = await cl.make_async(agent.run)(message)

    # Send a response back to the user
    await cl.Message(
        content=response["answers"][0].answer
    ).send()

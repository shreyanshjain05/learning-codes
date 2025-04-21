import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

async def main():
    load_dotenv()

    client = MCPClient.from_config_file(
        os.path.join("browser_mcp.json")
    )

    # Use a chat model that supports bind_tools
    llm = ChatGroq(model="llama3-8b-8192")
    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30)


    print('Chat Initialised...')
    print('Type Exit or Quit to end the conversation')
    print('Type Clear to start fresh')
    try:
        while True:
            user_input = input('You: ')
            if user_input.lower() in ['exit', 'quit']:
                print('Exiting...')
                break
            elif user_input.lower() == 'clear':
                print('Starting fresh...')
                continue
            else:
                  # Run the query
                result = await agent.run(
                   user_input,
                   max_steps=30,
                )
                print(f"\nResult: {result}")
    finally:
        if client and client.sessions():
            await client.close_sessions()
        print('Chat Ended...')

if __name__ == "__main__":
    asyncio.run(main())
import asyncio

from dotenv import load_dotenv
from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPAgent, MCPClient
import os

async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""
    # Load environment variables
    # load_dotenv()
    
    # Get API key from environment
    # api_key = os.getenv("GEMINI_API")
    api_key = "AIzaSyDT5vJw8jypaEsvZ77HNlVluWCrCKazZwQ"
    if not api_key:
        raise ValueError("GEMINI_API key not found in environment variables. Please set it in your .env file.")

    config_file = "browser_mcp.json"
    mcp_client = MCPClient.from_config_file(config_file)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key
    )

    agent = MCPAgent(
        llm=llm,
        client=mcp_client,
        max_steps=15,
        memory_enabled=True,
    )

    try:
        # Main chat loop
        while True:
            # Get user input
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # Check for clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        # Clean up
        if mcp_client and mcp_client.sessions:
            await mcp_client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
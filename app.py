import asyncio
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPAgent, MCPClient
import os, re
import time

async def classify_companies():
    try:
        # Load the Excel file
        print("Loading Excel file...")
        df = pd.read_excel('data.xls')
        
        # Create a new DataFrame for results
        results_df = pd.DataFrame(columns=['Company Name', 'Company Type', 'Reasoning'])
        
        # Define company types
        company_types = [
            "Wholesale Distribution",
            "Manufacturing",
            "Asset-Based Lending",
            "Freight & Transportation",
            "Business Services",
            "Transportation and Lodging",
            "Business and Professional Services",
            "Engineering & Construction"
        ]
        
        # Define 10 API keys
         # Define 10 API keys
        api_keys = [
            "AIzaSyAvFmMs0bZ_ujBI0bTeQJCZ7uP0WethAlc",  # Key 1
            "AIzaSyDvu8IL0taaKQD1tRBa-dLCmsLQZSdQqHk",  # Key 2
            "AIzaSyDASnL-ZxTMDlprPnYHUV8Oj7OOq6qOaME",  # Key 3
            "AIzaSyDTnWWoyjCZcsrMrk9AVVw1YKNPy-xmiSk",  # Key 4
            "AIzaSyCSoVtf8OPpjqa3bs2ZeLCVBExqZ1qapFM",  # Key 5
            "AIzaSyDy-Q4yt5UWo11GFhRyT96VxY3s-gsL97c",  # Key 6
            "AIzaSyD2WqDCIqb0-8umU4MxP4pkvvgLsPZmzDI",  # Key 7
            "AIzaSyAuvqB2UcAtj_kdSfE1Xt3ATFMopPe_pPI",  # Key 8
            "AIzaSyATgA0W8WgLzPZV5zczeHvdCitZUnmg0os",  # Key 9
            "AIzaSyBYowZjz3yfoM1DCwz1XtE91H5YouC3wVY"   # Key 10
        ]

        # Process each company name
        total_companies = len(df)
        processed_count = 0
        
        print("Company Classification Results:")
        print("="*50)
        
        for index, row in df.iterrows():
            company_name = row['Company  Name']
            if pd.isna(company_name):  # Skip empty cells
                continue
                
            processed_count += 1
        
            # Select API key based on row number
            current_api_key = api_keys[(processed_count - 1) % 10]
            
            # Create a prompt to search and classify the company
            prompt = f"""
            You are an expert for finding the key information about the company {company_name}
            
            After finding the key information, analyze the company's:
            1. Main business activities
            2. Services provided
            3. Industry sector
            4. Business model
            
            Available company types:
            {', '.join(company_types)}
            
            Based on the key information:
            1. If the company's main business matches any of the provided types, return that type
            2. If no match is found with the company type, return 'others'
            3. Always have to return the final answer"
            """
            
            try:
                # Initialize MCP client and agent with current API key
                config_file = "browser_mcp.json"
                mcp_client = MCPClient.from_config_file(config_file)
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    google_api_key=current_api_key
                )

                agent = MCPAgent(
                    llm=llm,
                    client=mcp_client,
                    max_steps=15,
                    memory_enabled=True,
                )
                
                # Get classification from the agent
            
                classification = await agent.run(prompt)
                
                # Clean up the response
                classification = classification.strip().lower()
                # print(f"Raw classification: {classification}")

                match = re.search(r"final answer:\s*(.+)", classification, re.IGNORECASE)
                if match:
                    final_answer = match.group(1)
                print("-"*50)
                print(f"Company Name: {company_name}")
                print(f"Company Type: {final_answer}")
                print("-"*50)
                
                # Add the result to the results DataFrame
                results_df = pd.concat([results_df, pd.DataFrame({
                    'Company Name': [company_name],
                    'Company Type': [final_answer],
                    'Reasoning': [classification]  # Store the full classification reasoning
                })], ignore_index=True)
                
                # Save after each classification
                results_df.to_csv('company_classifications.csv', index=False)
                print("Saved successfully!")
                
            except Exception as e:
                print(f"Error processing {company_name}: {str(e)}")
                # Print error result
                print("Company Type: others (Error)")
                print("-"*50)
                
                # Add error result to the results DataFrame
                results_df = pd.concat([results_df, pd.DataFrame({
                    'Company Name': [company_name],
                    'Company Type': ['others'],
                    'Reasoning': [f"Error occurred: {str(e)}"]  # Store the error message as reasoning
                })], ignore_index=True)
                print(f"Marked {company_name} as 'others' due to error")
                # Save even if there's an error
                results_df.to_csv('company_classifications.csv', index=False)
                print("Saved with error classification")
        
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
        
    finally:
        # Clean up
        if 'mcp_client' in locals() and mcp_client and mcp_client.sessions:
            print("Cleaning up MCP client sessions...")
            await mcp_client.close_all_sessions()

if __name__ == "__main__":
    try:
        asyncio.run(classify_companies())
    except Exception as e:
        print(f"Program terminated with error: {str(e)}")
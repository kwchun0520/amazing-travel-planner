import os  
from dotenv import load_dotenv
import streamlit as st
import asyncio
import datetime

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# LangChain LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Run MCP tool call
async def call_mcp_tool(user_query: str):
    # Define transport to MCP server
    transport = streamablehttp_client(url="http://127.0.0.1:8000/mcp")
    
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (reader, writer, _):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)

            # Bind tools to LLM
            agent = llm.bind_tools(tools)

            # Invoke the tool based on user input
            print(f"User query: {user_query}")
            result = await agent.ainvoke(user_query)
            print(f"Tool call result: {result}")
            return result.content

# Streamlit UI
st.title("🔍 Travel Planner Tool")

user_input = st.text_input("Enter a search query:")
        
# Country Input
country = st.text_input("Enter your desired country:")

# Date Input
travel_date = st.date_input("Select your travel date:", datetime.date.today())

# Hobbies Input (String)
hobbies = st.text_area("Tell us about your hobbies (comma-separated if multiple):",
                        help="e.g., hiking, photography, cooking")

# Travel Style Input (Dropdown)
travel_style_options = ["Adventure", "Relaxation", "Cultural Immersion", "Budget", "Luxury", "Family-friendly", "Romantic"]
travel_style = st.selectbox("Choose your travel style:", travel_style_options)

st.subheader("Your Selections:")
st.write(f"**Country:** {country if country else 'Not specified'}")
st.write(f"**Travel Date:** {travel_date}")
st.write(f"**Hobbies:** {hobbies if hobbies else 'Not specified'}")
st.write(f"**Travel Style:** {travel_style}")

if st.button("Submit"):
    st.success("Your travel preferences have been submitted!")
    # Here you could add logic to process the inputs,
    # e.g., save to a database, call an API, etc.
    if user_input.strip():
        result = asyncio.run(call_mcp_tool(user_input))
        st.markdown("### 🔎 Result:")
        st.write(result)
    else:
        st.warning("Please enter a valid query.")
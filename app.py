import streamlit as st
import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.googlesearch import GoogleSearch
import phi
import markdown
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Initialize Phi API key
phi.api_key = os.getenv("PHI_API_KEY")

# Initialize Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id="llama3-70b-8192"),
    tools=[GoogleSearch()],
    instructions=[
        "Always include sources",
        "Use tables to display the data for comparison",
        "Use source www.gadgets360.com only",
        "Show release year as well in case of gadgets search",
        "Always sort gadgets by year, also show gadgets list with price and release year"
        "Fetch gadgets details updated and latest year"
        "List gadgets from latest year to oldest year",
        "Behave like you are shopping consultant",
        "Don't use other sources except Gadgets360",
        "parse response as html table",
        "Show gadgets360 url wherever possible in news and gadgets details link", 
        "if data not available from Gadgets360 then don't show the data"
    ],
    show_tools_calls=True,
    markdown=True,
)

# Streamlit App
st.title("Gadgets360 AI Shopping Consultant")
st.write("This AI Chatbot resolve your query reagrding shopping, tech news and provides information from **Gadgets360**.")

# User Input
query = st.text_input("Enter your query:", value="")



def search(query):
    try:
        response = web_search_agent.run(query, stream=False)
        st.write(response.content)  # Display the response content
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Create a text input for user query
    #query = st.text_input("Enter your search query", "")

# Trigger the search when the user either presses Enter or clicks the button
if query:  # This condition is met when the user presses Enter after typing the query
    with st.spinner("Searching..."):
        search(query)

# Optionally, you can still keep the button for manual submission
if st.button("Search"):
    with st.spinner("Searching..."):
        search(query)

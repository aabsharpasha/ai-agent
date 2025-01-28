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
        "you are shopping consultant and have to assist your customer in shopping",
        "Always include sources",
        "Use tables to display the data for comparison",
        "Always sort gadgets by year, also show gadgets list with price and release year"
        "Show phone from last 1 years only. Must show current year phone first",
        "Don't use other sources except Gadgets360",
        "Parse response as html table",
        "Show gadgets360 corresponding device and news url wherever possible in news and gadgets details link", 
        "if data not available from Gadgets360 then don't show the data",
        "Must not show any data from other sources exept gadgets360",
        "Price must be shown in INR",
        "Always include Gadgets360 home page link saying visit for more information",
        "while comparision always show your verdict basis on price and specs"
        "Always show the latest news first",
        "Always show latest phones first",
        "Include phones current year and last year only",
        "Show mobiles with images if available"
        "Sort phones by release year",
        "Fetch phones for current and last year only"
        "Don't show phones older than 1 years",
    ],
    show_tools_calls=True,
    markdown=True,
)

# Streamlit App
st.title("Gadgets360 AI Shopping Consultant")
st.write("This AI Chatbot resolve your query reagrding shopping, tech news and provides information from **Gadgets360**.")



def search(query):
    try:
        response = web_search_agent.run(query, stream=False)
        st.empty()
        st.write(response.content)  # Display the response content
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Create a text input for user query
    #query = st.text_input("Enter your search query", "")

# User Input
col1, col2 = st.columns([4, 1])  # Adjust column widths as needed

with col1:
   query = st.text_input("Enter your query:", value="",key="search_input")

with col2:
    st.markdown("<div style='height: 1.3em;'></div>", unsafe_allow_html=True)  # Add vertical space to align
    if st.button("Search"):
        with st.spinner("Searching..."):
            st.empty()
            search(query)

if query:  # This condition is met when the user presses Enter after typing the query
    with st.spinner("Searching..."):
        st.empty()
        search(query)


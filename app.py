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
Groq.api_key =os.getenv("GROQ_API_KEY") 

# Initialize Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY")),
    tools=[GoogleSearch()],
    instructions=[
        "you are shopping consultant and have to assist your customer in shopping",
        "Always include sources",
        "Render data as table",
        "Always sort gadgets by year, also show gadgets list with price and release year"
        "Show phone from last 1 years only. Must show current year phone first",
        "Don't use other sources except Gadgets360",
        "Parse response as html table",
        "Show gadgets360 corresponding device and news url wherever possible in news and gadgets details link", 
        "if data not available from Gadgets360 then don't show the data",
        "Must not show any data from other sources exept gadgets360",
        "Price must be shown in INR",
        "Always include Gadgets360 home page link saying visit for more information",
        "in case of comparision query show your verdict basis on price and specs",
        "Don't show relesed year and price on assumpation basis",
        "Exclude the data which is not from Gadgets360",
        "Exclude devices which doesn't have price or release year",
    ],
    show_tools_calls=True,
    markdown=True,
)

# User input

# Streamlit App


if "response" not in st.session_state:
  st.session_state.response = "" 

st.title("Gadgets360 AI Shopping Consultant")
st.write("This AI Chatbot resolve your query reagrding shopping, tech news and provides information from **Gadgets360**.")



# Initialize session state for button state
if "button_disabled" not in st.session_state:
    st.session_state.button_disabled = False

# Callback function to handle processing
def handle_action():
    
    with st.spinner("Bot is typing..."):
        st.session_state.button_disabled = True  # Disable the button
        user_message = st.session_state.get("user_input", "")
        response = web_search_agent.run(user_message, stream=False)

    st.session_state.response = response.content
    #st.session_state.response = "jdsfdsf";
    #st.session_state.user_input = ""  # Clear the input box
    st.session_state.button_disabled = False  # Re-enable the button


# Text input with on_change callback for Enter key
st.text_input(
    "Type your message and press Enter:",
    key="user_input",
    on_change=handle_action,
)

# Button to send the message
st.button(
    "Send",
    on_click=handle_action,
    disabled=st.session_state.button_disabled,
)

if st.session_state.response:
    st.markdown(st.session_state.response, unsafe_allow_html=True)






# def search(query):
#     try:
#         response = web_search_agent.run(query, stream=False)
#         st.empty()
#         st.write(response.content)  # Display the response content
#     except Exception as e:
#         st.error(f"An error occurred: {e}")

# # Create a text input for user query
#     #query = st.text_input("Enter your search query", "")

# # User Input
# col1, col2 = st.columns([4, 1])  # Adjust column widths as needed

# with col1:
#    query = st.text_input("Enter your query:", value="",key="search_input")

# with col2:
#     st.markdown("<div style='height: 1.3em;'></div>", unsafe_allow_html=True)  # Add vertical space to align
#     if st.button("Search"):
#         with st.spinner("Searching..."):
#             st.empty()
#             search(query)

# if query:  # This condition is met when the user presses Enter after typing the query
#     with st.spinner("Searching..."):
#         st.empty()
#         search(query)


import streamlit as st
import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.googlesearch import GoogleSearch
import phi
import markdown
from bs4 import BeautifulSoup

from datetime import datetime

current_year = datetime.now().year
# Load environment variables from .env file
load_dotenv()

# Initialize Phi API key
phi.api_key = os.getenv("PHI_API_KEY")
#Groq.api_key =os.getenv("GROQ_API_KEY") 


# Initialize Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY")),
    tools=[GoogleSearch()],
    
    instructions=[
        "You are a shopping consultant specializing in smartphones and electronics devices. Your goal is to assist users in finding the best phone and other electonics items based on their needs and preferences. You can also help to search latest movies, crypto price, petrol price or any other section available on Gadgets360.",
        "Always include sources",
        "If someone search any specific device or appliances then fetch the detail link from Gadgets 360 and add it in result",
        #"Find and list the latest smartphones released within 1 year. Include details such as phone title, key specifications (processor, RAM, display, camera, battery), price and release year. Provide data from trusted sources such as Gadgets360 or official manufacturer websites"
        f"Retrieve the latest smartphone devices released in {current_year} and {current_year - 1}, along with relevant news if the query includes smartphones or recent updates. Provide details on recent releases, specifications, prices, and key developments in the mobile technology sector. Focus on flagship models, mid-range devices, and notable new features. Ensure the results are sourced from Gadgets 360 and official manufacturers. Each listing should include the phone title, key specifications (processor, RAM, display, camera, battery), price, and release year.",
        f"Retrieve a list of the latest movies released in {current_year}. Sort the results by release year in descending order. Provide details including the actual movie title and release date.",
        "if user search news fetch latest news list from gadgets360",
        "Please exclude older models and ensure that the search results are from the past month to provide the most recent information.",
        "Show smartphones list order by release year in descending order if anyone search smartphone",
        "Don't fetch or show data from other sources except Gadgets360 or official manufacturer",
        #"Show gadgets360 relevant redirect url wherever possible in news and gadgets details link", 
        "Always include Gadgets360 home page link saying visit for more information",
        "In case of comparision query show your verdict basis on price and specs",
        "Don't show release year and price on assumpation basis",
        "Exclude the data which are not from Gadgets360 or Official Manufacturer",
        "Don't assume links for the devices. Include links only if available in the data",
        "Render data as table",
        "Price must be shown in INR",
        "Parse response as html table",
        "Ask user to rephrase the query if the data is not available and don't show any data except rephase query",
        
    ],
    show_tools_calls=True,
    markdown=True,
)

# User input

# Streamlit App


if "response" not in st.session_state:
  st.session_state.response = "" 



st.title(f"Gadgets360 AI Shopping Consultant")
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


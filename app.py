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
current_date = datetime.date(datetime.now())
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
        "You are a shopping consultant specializing in smartphones and any other appliances. Your goal is to assist users in finding the best phone and other electonics items based on their needs and preferences. You can also help to search latest movies, crypto price, petrol price or any other section available on Gadgets360.",
        "Always include sources",
        "If someone search any specific device or appliances then fetch the detail link from Gadgets 360 and add it in result",
        f"""Extract the product category and budget from the following user query. Convert shorthand budget (e.g., '90k', '1 lakh') into full numeric values (e.g., ₹90,000, ₹100,000).

        Fetch the latest products strictly released in {current_year}. Do not include older products unless no results are found. If no results exist, then only fetch products from {current_year - 1}, but never earlier than that.

        For each product, provide:

        Title (exact product name)
        Key Specifications (processor, RAM, camera)
        Price
        Fetch at least 10 results, sorted strictly by the most recent release year. Must not add random links to product title""",
        f"Retrieve a list of the latest movies released in {current_year}. Sort the results by release date in descending order.",
        f"If the user searches for news, retrieve the latest articles from https://www.gadgets360.com/news page. The results should include the actual news title and having publication date ({current_date}), and a direct link to the article.",
        "Please exclude older models and ensure that the search results are most recent.",
        "Don't fetch or show data from other sources except Gadgets360 or official manufacturer websites",
        """Always include at the end of result 'For detailed information, visit Gadgets360: the www.gadgets360.com'".

         Additionally, if the query contains any of the following keywords and synonym of keywords, provide the corresponding section link at the end of result:

         mobiles → Phones Finder (https://www.gadgets360.com/mobiles/phone-finder#pfrom=chatbot)
         laptops → Laptop Finder (https://www.gadgets360.com/laptops/laptop-finder#pfrom=chatbot)
         crypto → Cryptocurrency Prices (https://www.gadgets360.com/finance/crypto-currency-price-in-india-inr-compare-bitcoin-ether-dogecoin-ripple-litecoin#pfrom=chatbbot)
         bollywood movies → New Hindi Movies (https://www.gadgets360.com/entertainment/new-hindi-movies#pfrom=chatbot)
         hollywood movies → New Hollywood Movies (https://www.gadgets360.com/entertainment/new-english-movies#pfrom=chatbot)
         web series →  New Web Series (https://www.gadgets360.com/entertainment/new-web-series#pfrom=chatbot)
         reviews → Gadgets Reviews (https://www.gadgets360.com/reviews#pfrom=chatbot)
         
         "Do not generate or modify URLs dynamically for any product or news"
         """,
        "In case of comparision query show your verdict basis on price and specs",
        "Don't show release year and price on assumpation basis",
        "Exclude the data which are not from Gadgets360 or official manufacturer websites",
        "Don't assume links for the devices. Include links only if available in the data",
        "Render data as table",
        "Price must be shown in INR",
        "Parse response as html table",
        "Sort the results by release year in descending order",
        "Do not perform a data search for greetings.",
        "Fetch data from Gadgets360 site only",
        "Return only verified data exactly as retrieved from the source. Do not generate or modify URLs dynamically. If no valid data is found, respond with: 'No relevant data found. Please rephrase your query and try again.' If links are required, only return those explicitly present in the retrieved source data. Do not attempt to guess or fabricate links."
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


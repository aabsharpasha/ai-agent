import openai
from phi.agent import Agent
import phi.api
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.googlesearch import GoogleSearch
from dotenv import load_dotenv
from phi.model.groq import Groq

import os
import phi
from phi.playground import Playground, serve_playground_app
# Load environment variables from .env file
load_dotenv()

phi.api=os.getenv("PHI_API_KEY")

## web search agent
web_search_agent=Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id="llama3-70b-8192"),
    tools=[GoogleSearch()],
    instructions=["Always include sources","Use tables to display the data for comaparision","use source www.gadgets360.com only", "show release year as well in case of gagdets search", "always sort gadgets by year, also show gadgets list with price and release year",  "Show gadgets360 url wherever possible in news and gadgets details link", "if data not availbe from Gadgets360 then don't show the data"],
    show_tools_calls=True,
    markdown=True,

)

## Financial agent
finance_agent=Agent(
    name="Finance AI Agent",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True,
                      company_news=True),
    ],
    instructions=["Use tables to display the data"],
    show_tool_calls=True,
    markdown=True,

)

app=Playground(agents=[web_search_agent]).get_app()

if __name__=="__main__":
    serve_playground_app("playground:app",reload=True)


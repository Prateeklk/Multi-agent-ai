from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = "KEY"

## Web search agent
web_search_agent = Agent(
    name = "web_search_agent",
    role = "Search the web for the information",
    model = Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[DuckDuckGo()],
    inputs=dict(query="What is the history of Bitcoin?"),
    instructions=['Always include the source'],
    show_tools_calls=True,
    markdown = True,
)

## Financial Agent
finance_agent = Agent(
    name = "Finance AI agent",
    model = Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news = True)
        ],
    instructions=['Use tables to display the data'],
    show_tool_calls = True,
    markdown = True,

)

multi_ai_agent=Agent(
    team=[web_search_agent,finance_agent],
    model=Groq(id="llama-3.1-70b-versatile"),
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

## Run the agent

multi_ai_agent.print_response("Summaries analyst recommendation and share the latest new for Apple", stream = True)


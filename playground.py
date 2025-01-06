from phi.agent import Agent
import phi.api
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
from phi.model.groq import Groq

import os
import phi 
from phi.playground import Playground, serve_playground_app

load_dotenv()

phi.api = os.getenv("PHI_API_KEY")

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

app = Playground(agents = [finance_agent, web_search_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app",reload=True)
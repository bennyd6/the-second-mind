from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Hardcode the API key
api_key = "AIzaSyAC9CEk8Hx2GBkChK4-Y-jQiEpHP0B5WrM"

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

# Run a basic query
response = llm.invoke([HumanMessage(content="What is LangChain?")])
print(response.content)

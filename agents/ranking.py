import requests
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from colorama import Fore, Style

# 🔐 API Keys
GEMINI_API_KEY = "AIzaSyDfdyyRwBDSMcCA9NlA6XCqtFH4r3Sy92w"
SERPAPI_KEY = "a42c2442b00c4a5146d54288fab5ea3ddc8213b867a51420b59bb0079fbff4d1"

# Function to print status messages with color
def print_status(message, color=Fore.GREEN):
    print(color + message + Style.RESET_ALL)

# Function to fetch ranking-related real-time data
def fetch_ranking_data(hypothesis):
    print_status(f"\nFetching ranking data for: {hypothesis[:50]}...", Fore.CYAN)
    
    url = f"https://serpapi.com/search.json?q={hypothesis}&api_key={SERPAPI_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        print_status("Error: Failed to fetch ranking data.", Fore.RED)
        return "No real-world data available."

    data = response.json()
    search_summaries = [result["snippet"] for result in data.get("organic_results", [])[:3]]

    if search_summaries:
        print_status(f"Found {len(search_summaries)} relevant ranking points!", Fore.GREEN)
        return "\n".join(search_summaries)
    else:
        print_status("No relevant ranking data found.", Fore.YELLOW)
        return "No real-world data available."

# Function to rank the hypothesis
def rank_hypothesis(hypothesis):
    print_status("\nScoring hypothesis based on feasibility, cost, impact, and adoption...", Fore.BLUE)
    
    ranking_data = fetch_ranking_data(hypothesis)

    print_status("\nAnalyzing scores with Gemini AI...", Fore.CYAN)
    time.sleep(2)  # Simulate AI processing delay

    # 🔥 LangChain Gemini model
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

    # 📜 Ranking Prompt
    prompt = f"""
    Hypothesis: {hypothesis}

    Real-World Data for Ranking:
    {ranking_data}

    Task: Assign a score (0-10) for each of the following factors:
    - Feasibility: How realistic is the hypothesis technically?
    - Cost-effectiveness: Does it offer a good balance of cost vs. benefit?
    - Impact: How beneficial is it to society/environment?
    - Adoption Potential: Are people/industries adopting it?

    Provide a total score (out of 10) and categorize it as:
    - High Feasibility (8-10)
    - Medium Feasibility (5-7)
    - Low Feasibility (0-4)

    Explain your ranking.
    """

    response = model.invoke(prompt)

    print_status("\nRanking completed!\n", Fore.GREEN)
    return response.content if response else "Error in ranking analysis."
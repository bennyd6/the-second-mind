import time
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from colorama import Fore, Style

# 🔐 API Keys
GEMINI_API_KEY = "AIzaSyDfdyyRwBDSMcCA9NlA6XCqtFH4r3Sy92w"
SERPAPI_KEY = "a42c2442b00c4a5146d54288fab5ea3ddc8213b867a51420b59bb0079fbff4d1"

# ✅ Function to Print Status Updates
def print_status(message, color=Fore.GREEN):
    print(color + message + Style.RESET_ALL)

# 🌍 Fetch Latest Trends from Web
def fetch_latest_trends(hypothesis):
    print_status("\n🔍 Fetching latest trends related to the hypothesis...", Fore.BLUE)
    
    url = f"https://serpapi.com/search.json?q={hypothesis} latest trends&api_key={SERPAPI_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print_status("Error: Failed to fetch latest trends.", Fore.RED)
        return "No recent trends found."
    
    data = response.json()
    trends = [result["snippet"] for result in data.get("organic_results", [])[:3]]
    
    if trends:
        print_status(f"Found {len(trends)} recent trends!", Fore.GREEN)
        return "\n".join(trends)
    else:
        print_status("No major trends found.", Fore.YELLOW)
        return "No recent trends found."

# 🚀 Evolution Agent: Enhances Hypothesis Based on Latest Data
def evolve_hypothesis(reflection_analysis, query ,ranking_analysis):
    print_status("\n🌱 Evolving the hypothesis with real-world insights...", Fore.CYAN)
    
    latest_trends = fetch_latest_trends(query)
    
    print_status("\n🤖 Refining hypothesis using AI...")
    time.sleep(2)  # Simulate AI processing delay
    
    # 🔥 LangChain Gemini Model
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)
    
    # 📜 Evolution Prompt
    prompt = f"""

    **Reflection Analysis Outcome:**  
    {reflection_analysis}  

    **Ranking Analysis Outcome:**  
    {ranking_analysis}  

    **Latest Trends & Real-World Updates:**  
    {latest_trends}  

    **Task:**  
    - **Enhance** the hypothesis based on all collected insights.  
    - Ensure it aligns with **latest trends**, **technical feasibility**, and **practical adoption**.  
    - If needed, **modify the hypothesis** while keeping its core idea intact.  

    **Output:**  
    Provide only the **evolved hypothesis** after analysis.  
    """

    response = model.invoke(prompt)
    
    print_status("\n✅ Hypothesis evolution completed!", Fore.GREEN)
    return response.content if response else "❌ Error in hypothesis evolution."

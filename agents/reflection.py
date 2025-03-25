import time
import requests
from colorama import Fore
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI


# 🔑 Google Gemini API Key
GEMINI_API_KEY = "AIzaSyAC9CEk8Hx2GBkChK4-Y-jQiEpHP0B5WrM"

# ✅ Function to Print Status Updates
def print_status(message, color):
    print(color + message + Fore.RESET)

# 🔍 Fetch Research Papers from Google Scholar
def fetch_google_scholar_papers(hypothesis):
    print_status("\n🔍 Searching Google Scholar for related research...", Fore.BLUE)
    
    query = hypothesis.replace(" ", "+")  # Format query for search
    url = f"https://scholar.google.com/scholar?q={query}"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".gs_rt a")  # Extract titles of research papers
        
        papers = [{"title": result.text, "link": result["href"]} for result in results[:5]]
        return papers if papers else [{"title": "No relevant research papers found.", "link": "#"}]
    else:
        return [{"title": "Error fetching Google Scholar results.", "link": "#"}]

# ✅ Fetch Fact-Checking Data
def fetch_fact_check_results(hypothesis):
    print_status("\n✅ Checking fact-checking sources...", Fore.YELLOW)
    
    # Dummy response (Replace with API if needed)
    fact_checks = [
        {"source": "Snopes", "verdict": "Mostly True"},
        {"source": "PolitiFact", "verdict": "Partially Accurate"},
        {"source": "FactCheck.org", "verdict": "No relevant claims found."}
    ]
    
    return fact_checks

# 📰 Fetch News Articles
def fetch_news_results(hypothesis):
    print_status("\n📰 Searching news sources for real-world relevance...", Fore.MAGENTA)
    
    # Dummy response (Replace with API if needed)
    news_articles = [
        {"title": "TechCrunch: New study shows solar window panels outperform rooftop panels.", "source": "TechCrunch"},
        {"title": "BBC News: Renewable energy innovations gain traction globally.", "source": "BBC"},
        {"title": "No recent news articles available on this hypothesis.", "source": "Unknown"}
    ]
    
    return news_articles

# 🔍 Fetch Validation Data from All Sources
def fetch_validation_data(hypothesis):
    print_status("\n🔍 Fetching real-world validation data...", Fore.BLUE)
    
    return {
        "research_papers": fetch_google_scholar_papers(hypothesis),
        # "fact_checks": fetch_fact_check_results(hypothesis),
        # "news_articles": fetch_news_results(hypothesis),
    }

# 🤖 Reflection Agent: Validates & Refines Hypothesis
def reflect_on_hypothesis(hypothesis):
    print_status("\n🔍 Validating hypothesis using real-world data...", Fore.BLUE)
    
    # 🌍 Fetch real-world evidence
    real_world_data = fetch_validation_data(hypothesis)

    print_status("\n🔬 Performing logical consistency check...", Fore.CYAN)
    time.sleep(2)  # Simulate AI processing delay

    # 🔥 LangChain Gemini Model
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)



    prompt = f"""
    **Initial Hypothesis:**  
    {hypothesis}  

    **Validation Data from Web:**  
    📚 **Research Papers:**  
    {', '.join([f"{p['title']} ({p['link']})" for p in real_world_data['research_papers']])}  

    **Task:**  
    - **Analyze** the hypothesis based on logical consistency and real-world evidence.  
    - **Classify it** as **"Valid"**, **"Partially Valid"**, or **"Invalid"** with a reason.  
    - **Refine** the hypothesis if necessary, ensuring it aligns with the latest data.  

    **Output:**  
    Provide only the **refined hypothesis** after analysis.  
    """

    # 🧠 Get response from Gemini
    response = model.invoke(prompt)

    print_status("\n✅ Reflection analysis completed!\n", Fore.GREEN)
    
    return response.content if response else "❌ Error in reflection analysis."


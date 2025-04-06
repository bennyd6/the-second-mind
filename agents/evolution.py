import os
import time
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv(".env")

GEMINI_API_KEY = os.getenv("gemini_api")
SERPAPI_KEY = os.getenv("serp_api")

if not GEMINI_API_KEY or not SERPAPI_KEY:
    raise ValueError("Missing API keys! Ensure GEMINI_API_KEY and SERPAPI_KEY are set.")

def fetch_latest_trends(hypothesis):
    url = f"https://serpapi.com/search.json?q={hypothesis} latest trends&api_key={SERPAPI_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        trends = [result.get("snippet", "No summary available.") for result in data.get("organic_results", [])[:3]]
        if trends:
            return "\n".join(trends)
        else:
            return "No recent trends found."
    except requests.exceptions.RequestException:
        return "No recent trends found."

def evolve_hypothesis(reflection_analysis, query, ranking_analysis):
    latest_trends = fetch_latest_trends(query)
    time.sleep(2)
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)
    prompt = f"""
    **Reflection Analysis Outcome:**  
    {reflection_analysis}  

    **Ranking Analysis Outcome:**  
    {ranking_analysis}  

    **Latest Trends & Real-World Updates:**  
    {latest_trends}  

    **Task:**  
    - **Enhance** the hypothesis by incorporating insights from all data sources.  
    - Ensure it aligns with **latest trends**, **technical feasibility**, and **practical adoption**.  
    - If necessary, **refine the hypothesis** while maintaining its core idea.  

    **Output Format:**  
    ```
    Evolved Hypothesis: [Refined hypothesis here]  
    Explanation: [Brief reason for modification]  
    ```
    """
    try:
        response = model.invoke(prompt)
        evolved_hypothesis = response.content if response else "Error in hypothesis evolution."
        return evolved_hypothesis
    except Exception:
        return "Error in hypothesis evolution."

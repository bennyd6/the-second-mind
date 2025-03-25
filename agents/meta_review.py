import time
from colorama import Fore, Style
from langchain_google_genai import ChatGoogleGenerativeAI

# 🔑 Google Gemini API Key
GEMINI_API_KEY = "AIzaSyAC9CEk8Hx2GBkChK4-Y-jQiEpHP0B5WrM"

# ✅ Function to Print Status Updates
def print_status(message, color=Fore.MAGENTA):
    print(color + message + Style.RESET_ALL)

# 📌 Meta-Review Agent
def meta_review(generation_output, reflection_feedback, ranking_analysis, evolution_output, proximity_relevance):
    print_status("\n🔎 Running Meta-Review to evaluate the entire pipeline...", Fore.YELLOW)
    time.sleep(2)

    # 🤖 Gemini Model (for review analysis)
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

    # 📝 Review Prompt
    prompt = f"""
    **Meta-Review: Evaluating AI Pipeline**  

    **Generation Agent Output:**  
    {generation_output}  

    **Reflection Agent Feedback:**  
    {reflection_feedback}  

    **Ranking Agent Analysis:**  
    {ranking_analysis}  

    **Evolution Agent Output:**  
    {evolution_output}  

    **Proximity Agent Relevance Check:**  
    {proximity_relevance}  

    **Task:**  
    - **Analyze Efficiency:** Were there delays, bottlenecks, or redundant steps?  
    - **Check Accuracy:** Did the outputs align with real-world data?  
    - **Identify Weaknesses:** Which agent underperformed, and why?  
    - **Suggest Improvements:** Provide 3 clear optimization strategies.  
    - **Final Score:** Rate the overall pipeline from **1 to 10** (based on speed, accuracy, and coherence).  

    **Output:**  
    - Give the final hypothesis and analysis considering every point above
    """

    # 🧠 Get Meta-Review Response
    response = model.invoke(prompt)

    print_status("\n✅ Meta-Review Completed!\n", Fore.GREEN)
    return response.content if response else "❌ Error in Meta-Review Analysis."

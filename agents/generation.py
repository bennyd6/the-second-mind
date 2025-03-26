import requests
import time
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from colorama import Fore, Style

# 🔐 Hardcoded API Keys (Replace with valid keys)
GEMINI_API_KEY = "AIzaSyDfdyyRwBDSMcCA9NlA6XCqtFH4r3Sy92w"
SERPAPI_KEY = "a42c2442b00c4a5146d54288fab5ea3ddc8213b867a51420b59bb0079fbff4d1"

# Function to print status messages with color
def print_status(message, color=Fore.GREEN):
    print(color + message + Style.RESET_ALL)

# Function to fetch top 3 search results
def web_scrape(topic):
    print_status(f"\nSearching for: {topic}...", Fore.CYAN)
    
    url = f"https://serpapi.com/search.json?q={topic}&api_key={SERPAPI_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        print_status("Error: Failed to fetch search results.", Fore.RED)
        return []

    data = response.json()
    search_results = [result["link"] for result in data.get("organic_results", [])[:3]]

    if search_results:
        print_status(f"Found {len(search_results)} relevant articles!", Fore.GREEN)
    else:
        print_status("No articles found.", Fore.YELLOW)

    return search_results

# Function to extract ALL paragraphs from a given URL
def extract_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print_status(f"Fetching content from: {url}...", Fore.MAGENTA)
    time.sleep(1)  # Simulate loading delay

    try:
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            print_status(f" Skipping {url} (Status: {response.status_code})", Fore.YELLOW)
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")  # Extract ALL paragraphs
        text_content = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])
        
        if text_content:
            print_status(" Successfully extracted content!", Fore.GREEN)
        else:
            print_status(" No readable content found.", Fore.YELLOW)

        return text_content
    
    except requests.exceptions.RequestException:
        print_status(f" Skipping {url} due to a request error.", Fore.RED)
        return ""

# Function to generate hypothesis using Gemini
def generate_hypothesis(topic):
    web_results = web_scrape(topic)

    if not web_results:
        print_status(" No relevant articles found. Exiting...", Fore.RED)
        return "No hypothesis generated."

    print_status("\n Extracting information from articles...", Fore.BLUE)

    # Collect content from all top 3 links
    extracted_content = []
    for url in web_results:
        content = extract_content(url)
        if content:
            extracted_content.append(content)

    if not extracted_content:
        content = "No relevant data found."
        print_status(" No usable content from articles.", Fore.YELLOW)
    else:
        content = "\n\n".join(extracted_content)
        print_status(" Content successfully gathered!", Fore.GREEN)

    print_status("\n Generating hypothesis using Gemini AI...", Fore.CYAN)
    time.sleep(2)  # Simulate AI processing delay

    # 🔥 LangChain Gemini model
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

    # 📜 Prompt for hypothesis generation
    prompt = f"""
    Topic: {topic}
    Extracted Web Content:
    {content}

    Generate a structured analysis based on this information.
    """

    response = model.invoke(prompt)

    print_status("\n Hypothesis generated successfully!\n", Fore.GREEN)
    return response.content if response else "Error generating hypothesis."
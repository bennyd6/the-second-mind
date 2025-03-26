import faiss
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer
from colorama import Fore, Style

# Initialize colorama
print(Fore.CYAN + "🔄 Initializing Proximity Analysis Module..." + Style.RESET_ALL)

# Load the Sentence Transformer model
print(Fore.YELLOW + "📥 Loading Sentence Transformer model..." + Style.RESET_ALL)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print(Fore.GREEN + "✅ Model loaded successfully!" + Style.RESET_ALL)

# FAISS Setup
D = 384  # Embedding dimension
print(Fore.YELLOW + f"🛠️ Setting up FAISS with dimension {D}..." + Style.RESET_ALL)
index = faiss.IndexFlatIP(D)  # Cosine similarity index
print(Fore.GREEN + "✅ FAISS initialized!" + Style.RESET_ALL)

# Load saved FAISS index, queries, and responses
if os.path.exists("faiss_data.json"):
    print(Fore.YELLOW + "📂 Loading existing FAISS data..." + Style.RESET_ALL)
    with open("faiss_data.json", "r") as f:
        data = json.load(f)
        queries = data["queries"]
        responses = data["responses"]
    print(Fore.GREEN + "✅ FAISS data loaded!" + Style.RESET_ALL)
else:
    print(Fore.RED + "⚠️ No existing FAISS data found. Initializing fresh storage..." + Style.RESET_ALL)
    queries = []
    responses = {}

# Try to load FAISS index
if os.path.exists("faiss_index.bin"):
    print(Fore.YELLOW + "📂 Loading FAISS index..." + Style.RESET_ALL)
    index = faiss.read_index("faiss_index.bin")
    print(Fore.GREEN + "✅ FAISS index loaded!" + Style.RESET_ALL)
else:
    print(Fore.RED + "⚠️ No FAISS index found. Creating a new one..." + Style.RESET_ALL)
    index = faiss.IndexFlatIP(D)

def get_embedding(text):
    """Generate a normalized embedding for cosine similarity."""
    print(Fore.BLUE + f"🔍 Generating embedding for query: {text}" + Style.RESET_ALL)
    embedding = embedding_model.encode(text).astype("float32")
    norm_embedding = embedding / np.linalg.norm(embedding)
    print(Fore.GREEN + "✅ Embedding generated!" + Style.RESET_ALL)
    return norm_embedding

def search_faiss(query_vector, threshold=0.85):
    """Search FAISS for a similar query and return the closest match."""
    print(Fore.BLUE + "🔍 Searching FAISS for similar queries..." + Style.RESET_ALL)
    if index.ntotal == 0:
        print(Fore.RED + "⚠️ No queries stored in FAISS!" + Style.RESET_ALL)
        return None, None  

    D, I = index.search(np.array([query_vector]), k=1)
    similarity = D[0][0]  # Cosine similarity (1 = perfect match)

    if similarity > threshold:
        print(Fore.GREEN + f"✅ Match found with similarity {round(similarity, 2)}!" + Style.RESET_ALL)
        return I[0][0], queries[I[0][0]]
    
    print(Fore.YELLOW + "⚠️ No similar query found." + Style.RESET_ALL)
    return None, None

def proximity_analysis(query, evolution_response):
    """Compare the new response with past stored responses and analyze changes."""
    print(Fore.CYAN + f"🔎 Analyzing proximity for query: {query}" + Style.RESET_ALL)
    query_vector = get_embedding(query)
    idx, matched_query = search_faiss(query_vector)

    if matched_query:
        past_response = responses[matched_query]
        analysis = f"""
        ✅ {Fore.GREEN}Found a similar past query:{Style.RESET_ALL} {matched_query}
        📌 {Fore.BLUE}Similarity Score:{Style.RESET_ALL} {round(idx, 2)}
        🔄 {Fore.MAGENTA}Past Response:{Style.RESET_ALL} {past_response}
        ⚡ {Fore.YELLOW}Evolution Response:{Style.RESET_ALL} {evolution_response}

        🔍 {Fore.CYAN}Analysis:{Style.RESET_ALL} The new response {("is similar" if past_response in evolution_response else "has significant changes")} 
        compared to the past response.
        """
    else:
        analysis = f"{Fore.YELLOW}⚠️ No similar past queries found. Using fresh response.{Style.RESET_ALL}"

    # Store the new query & response in FAISS
    print(Fore.YELLOW + "📥 Storing new query and response..." + Style.RESET_ALL)
    queries.append(query)
    responses[query] = evolution_response
    index.add(np.array([query_vector]).astype("float32"))
    print(Fore.GREEN + "✅ Query stored successfully!" + Style.RESET_ALL)

    # Save FAISS data
    with open("faiss_data.json", "w") as f:
        json.dump({"queries": queries, "responses": responses}, f)
    faiss.write_index(index, "faiss_index.bin")
    print(Fore.GREEN + "✅ FAISS data saved!" + Style.RESET_ALL)

    return analysis

import redis
from generation import generate_hypothesis
from reflection import reflect_on_hypothesis
from ranking import rank_hypothesis
from evolution import evolve_hypothesis
from proximity import proximity_analysis
from meta_review import meta_review
import google.generativeai as genai

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

genai.configure(api_key="AIzaSyDfdyyRwBDSMcCA9NlA6XCqtFH4r3Sy92w")
model = genai.GenerativeModel("gemini-2.0-flash")

def store_memory(query, response):
    """Store query and meta_review response in Redis."""
    index = redis_client.incr("query_index")
    redis_client.set(f"query:{index}", f"Query: {query}\nMeta Review: {response}")

def clear_memory():
    """Clear Redis memory."""
    keys = redis_client.keys("query:*")
    for key in keys:
        redis_client.delete(key)
    redis_client.delete("query_index")

def get_chat_history():
    """Retrieve past query-response pairs from Redis."""
    keys = sorted(redis_client.keys("query:*"))
    history = [redis_client.get(key) for key in keys]
    return "\n".join(history)

first_query = True

while True:
    query = input("Enter your query (or 'q' to quit): ")
    if query.lower() == 'q':
        print("Clearing memory and exiting...")
        clear_memory()
        break
    
    if first_query:
        generation = generate_hypothesis(query)
        print("Generated Hypothesis:", generation)
        
        reflection = reflect_on_hypothesis(generation)
        print("Reflection:", reflection)
        
        ranking = rank_hypothesis(reflection)
        print("Ranking:", ranking)
        
        evolution = evolve_hypothesis(reflection, query, ranking)
        print("Evolved Hypothesis:", evolution)
        
        proximity = proximity_analysis(query, evolution)
        print("Proximity Analysis:", proximity)
        
        meta_review_response = meta_review(generation, reflection, ranking, evolution, proximity)
    else:
        history = get_chat_history()
        prompt = f"Context:\n{history}\n\nUser: {query}\nBot:"
        meta_review_response = model.generate_content(prompt).text
    
    print("Meta Review:", meta_review_response)
    
    # Store query and meta_review response in Redis
    store_memory(query, meta_review_response)
    first_query = False
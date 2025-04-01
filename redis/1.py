from flask import Flask, request, jsonify
import redis
import google.generativeai as genai

# Flask app
app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyDfdyyRwBDSMcCA9NlA6XCqtFH4r3Sy92w")
model = genai.GenerativeModel("gemini-2.0-flash")

# Redis setup for short-term memory
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def get_chat_history(user_id):
    """Retrieve past conversations from Redis for a specific user."""
    keys = sorted(redis_client.keys(f"chat:{user_id}:*"))
    history = [redis_client.get(key) for key in keys]
    return "\n".join(history)

def store_memory(user_id, query, response):
    """Store query-response pairs in Redis."""
    index = redis_client.incr(f"chat:{user_id}:index")
    redis_client.set(f"chat:{user_id}:{index}", f"User: {query}\nBot: {response}")

def clear_memory(user_id):
    """Clear short-term memory for a user."""
    keys = redis_client.keys(f"chat:{user_id}:*")
    for key in keys:
        redis_client.delete(key)

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chat queries."""
    data = request.json
    user_id = data.get("user_id")
    query = data.get("query")
    clear_memory_flag = data.get("clear_memory", False)

    if clear_memory_flag:
        clear_memory(user_id)

    # Retrieve past conversations to maintain context
    past_conversations = get_chat_history(user_id) if not clear_memory_flag else ""
    prompt = f"Context:\n{past_conversations}\n\nUser: {query}\nBot:" if past_conversations else f"User: {query}\nBot:"

    # Generate response
    response = model.generate_content(prompt).text

    # Store memory if not a new chat
    if not clear_memory_flag:
        store_memory(user_id, query, response)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

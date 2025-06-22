import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS to handle cross-origin requests

# --- Flask App Initialization ---
app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing your web page to access it

# --- Configuration ---
API_KEY = "AIzaSyAVIs0mZFeTTz7WvsKWIXH3MLLUhad_-M4" # Replace with your actual key

genai.configure(api_key=API_KEY)

# --- Model Initialization ---
model = genai.GenerativeModel('gemini-1.5-flash')

# --- In-memory chat history (for demonstration) ---
# In a real-world public application, you would typically use a database
# to store chat histories for different users. For this example, we'll
# use a simple dictionary to store history per session ID.
chat_sessions = {}

# --- API Endpoint ---
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    """
    Handles chat requests from the web page.
    Expects a JSON payload like:
    {
        "message": "User's query",
        "session_id": "unique-id-for-user-session"
    }
    """
    try:
        data = request.get_json()
        user_input = data.get('message')
        session_id = data.get('session_id') # Get session ID from request

        if not user_input:
            return jsonify({"error": "No message provided"}), 400
        if not session_id:
            return jsonify({"error": "No session_id provided"}), 400

        # Get or create chat session for the given session_id
        if session_id not in chat_sessions:
            chat_sessions[session_id] = model.start_chat(history=[])
            print(f"New chat session created for ID: {session_id}")
        
        chat = chat_sessions[session_id]
        
        print(f"Received message for session {session_id}: {user_input}")

        # Send the user's message to the model
        response = chat.send_message(user_input)
        bot_response = response.text
        print(f"ShayaanGPT response for session {session_id}: {bot_response}")

        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error in chat_endpoint: {e}")
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

# --- Health Check Endpoint (Optional but good practice) ---
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})

# --- Run the Flask app ---
if __name__ == '__main__':
    # You might want to run this on a specific port, e.g., 5000
    # For development, you can run it directly: flask run
    # For a more robust deployment, use a WSGI server like Gunicorn/Waitress.
    app.run(host='0.0.0.0', port=5000, debug=True) # debug=True is for development only

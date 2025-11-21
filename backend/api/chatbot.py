from flask import jsonify, request
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def chatbot():
    user_message = request.args.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Use Gemini 1.5 Flash (text-only model)
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            f"You are SortSmart, a recycling assistant who helps people decide how to properly dispose of waste items. "
            f"Give short, friendly, and clear recycling tips.\n\nUser: {user_message}"
        )

        # Return the response text
        if hasattr(response, "text"):
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "No response received from Gemini."})

    except Exception as e:
        import traceback
        print("----- ERROR OCCURRED -----")
        traceback.print_exc()
        print("---------------------------")
        return jsonify({"error": str(e)}), 500

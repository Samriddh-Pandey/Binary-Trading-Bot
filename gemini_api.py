import google.generativeai as genai
from config import GEMINI_API_KEY

# Initialize the Gemini API client with the correct model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")  # or whatever model you're using

def get_prediction(currency_pair, timeframe):
    prompt = (
        f"pair: {currency_pair}. "
        f"expiry: {timeframe} minutes. type: binary"
        "suggest me an acurate trade for the next {timeframe} minutes just say up or down and nothing else."
    )

    # Send the prompt to the model and get the response
    response = model.generate_content(prompt)

    # Extract and clean the response
    prediction = response.text.strip().lower()
    return prediction

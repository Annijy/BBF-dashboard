import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API-avainta ei löytynyt .env-tiedostosta.")
    raise SystemExit

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Vastaa vain sanalla: toimii"
    )

    print("API-yhteys toimii.")
    print("Geminin vastaus:", response.text)

except Exception as error:
    print("API-yhteys ei toimi.")
    print(error)
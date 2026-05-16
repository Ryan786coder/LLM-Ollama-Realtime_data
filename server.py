from ollama import Client
import requests
import re
from typing import List



client = Client(host="http://localhost:11434")



def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=j1"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        response.raise_for_status()

        data = response.json()

        current = data["current_condition"][0]

        return (
            f"Temperature in {city} is "
            f"{current['temp_C']}°C and "
            f"{current['weatherDesc'][0]['value']}"
        )

    except requests.exceptions.JSONDecodeError:
        return "Error: API did not return valid JSON."

    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"

    except KeyError:
        return "Error: Weather data format changed."




def fetch_place_names(text: str):
    #places = ["Guwahati","Japan", "Mumbai"]
    res = []
    
    for match in text.split(' '):
        #for pl in places:
            #if match == pl:
                res.append(match)
    
    return res
   
        
def llm_fetching(text: str):
    SYSTEM_PROMPT= f"""
        Out of all words select only places name like city,state,country from {text}
    """
    resp = client.chat(
        model="gemma:2b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    )
    
    return resp.message.content

while True:

    user_input = input("\n\nHi, How can I help you?\n")

    if user_input.lower() == "exit":
        break

    filtered_ = fetch_place_names(user_input)

    print("\n\nSplitting ",filtered_,"\n\n")

    filtered_user_input = llm_fetching(filtered_)

    print("\n\nPlaces  ",filtered_user_input,"\n\n")

    #for list_input in filtered_user_input:
        
    weather_report = get_weather(filtered_user_input)

    response = client.chat(
        model="gemma:2b",
        messages=[
            {
                "role": "system",
                "content": "You are a weather assistant."
            },
            {
                "role": "user",
                "content": weather_report
            }
        ]
    )


    print("\nAI Response:")
    print(response.message.content)
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get user's last message
        # city = tracker.latest_message['text']
        # Make an API call to get the weather on the selected city
        # weather_data = self.get_weather(city)

        city_slot = next(tracker.get_latest_entity_values("city"), None)
        city = tracker.get_slot("city") or city_slot

        if city:
            weather_data = self.get_weather(city)
            print(f'City: {city}')
            print(f'Weather data: {weather_data}')

            if weather_data:
                response = (f"O tempo em {city} é {weather_data['main']['temp']}°C"
                            f"com {weather_data['weather'][0]['description']}")
            else:
                response = f"Desculpe-me. Não consegui obter informações meteorológicas para {city}..."
        else:
            response = f"Desculpe-me. Não consegui obter informações meteorológicas para {city}..."

        # Answer the user with a weather message or a not found message
        dispatcher.utter_message(text=response)

        return []

    @staticmethod
    def get_weather(city: str) -> Dict[Text, Any] | None:
        api_key = "7f30ba4cbd9d9dfca70e610e1d50bda6"
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "units": "metric",
            "appid": api_key
        }

        try:
            print(f"URL da API requisitada : {base_url}?{params}")

            response = requests.get(base_url, params=params)
            api_response = response.json()

            print(f"Resposta da API : {api_response}")

            return api_response
        except requests.exceptions.RequestException as ex:
            print(f"Houve um erro com a requisição à API : {ex}")
            return None
